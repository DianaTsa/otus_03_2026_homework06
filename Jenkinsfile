pipeline {
    agent any

    parameters {
        string(name: 'EXECUTOR_URL', defaultValue: 'http://selenoid:4444/wd/hub', description: 'Адрес Selenoid')
        string(name: 'BASE_URL', defaultValue: 'http://prestashop:80/', description: 'Адрес приложения')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Браузер')
        string(name: 'BROWSER_VERSION', defaultValue: '128.0', description: 'Версия браузера')
        string(name: 'THREADS', defaultValue: '1', description: 'Потоки')
    }

    environment {
        COMPOSE_PROJECT_NAME = "otus_hw06_${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/DianaTsa/otus_03_2026_homework06.git'
            }
        }

        stage('Prepare Infrastructure') {
            steps {
                sh '''
                    docker network inspect app_network >/dev/null 2>&1 || docker network create app_network
                    docker rm -f mysql_db prestashop prestashop_postinstall selenoid selenoid-ui selenoid_proxy pytest_runner 2>/dev/null || true
                    docker compose --profile tests --profile prestashop down -v --remove-orphans || true
                    docker compose --profile prestashop up -d db prestashop
                '''
            }
        }

        stage('Wait PrestaShop') {
            steps {
                sh '''
                    echo "Waiting for PrestaShop health..."

                    for i in $(seq 1 90); do
                        STATUS=$(docker inspect --format='{{json .State.Health.Status}}' prestashop 2>/dev/null || echo "null")
                        echo "Attempt $i. PrestaShop health: $STATUS"

                        if echo "$STATUS" | grep -q "healthy"; then
                            echo "PrestaShop container is healthy"
                            break
                        fi

                        if [ "$i" = "90" ]; then
                            echo "PrestaShop did not become healthy"
                            docker logs prestashop || true
                            exit 1
                        fi

                        sleep 10
                    done

                    echo "Running postinstall cleanup..."
                    docker compose --profile prestashop up prestashop_postinstall || true

                    echo "Checking PrestaShop HTTP..."
                    for i in $(seq 1 30); do
                        if docker run --rm --network app_network curlimages/curl:8.10.1 -fsS http://prestashop:80/ >/dev/null; then
                            echo "PrestaShop is available"
                            exit 0
                        fi

                        echo "Waiting HTTP... attempt $i"
                        sleep 5
                    done

                    echo "PrestaShop HTTP check failed"
                    docker logs prestashop || true
                    exit 1
                '''
            }
        }

        stage('Setup Selenoid') {
            steps {
                sh '''
                    echo "Setup Selenoid..."

                    if [ ! -f browsers.json ]; then
                        echo "ERROR: browsers.json not found"
                        exit 1
                    fi

                    BROWSER_VALUE="${BROWSER:-chrome}"
                    BROWSER_VERSION_VALUE="${BROWSER_VERSION:-128.0}"

                    echo "Pulling browser image..."
                    if [ "${BROWSER_VALUE}" = "chrome" ]; then
                        docker pull selenoid/vnc_chrome:${BROWSER_VERSION_VALUE}
                    elif [ "${BROWSER_VALUE}" = "firefox" ]; then
                        docker pull selenoid/vnc_firefox:${BROWSER_VERSION_VALUE}
                    else
                        echo "Unsupported browser: ${BROWSER_VALUE}"
                        exit 1
                    fi

                    docker compose --profile tests up -d selenoid
                    docker cp browsers.json selenoid:/etc/selenoid/browsers.json
                    docker restart selenoid

                    echo "Waiting for Selenoid..."
                    for i in $(seq 1 30); do
                        if docker run --rm --network app_network curlimages/curl:8.10.1 -fsS http://selenoid:4444/status >/dev/null; then
                            echo "Selenoid is available"
                            docker run --rm --network app_network curlimages/curl:8.10.1 -fsS http://selenoid:4444/status || true
                            exit 0
                        fi

                        echo "Waiting Selenoid... attempt $i"
                        sleep 3
                    done

                    echo "Selenoid did not start"
                    docker logs selenoid || true
                    exit 1
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    echo "Building and running tests..."

                    docker compose --profile tests build tests
                    docker rm -f pytest_runner 2>/dev/null || true

                    BROWSER_VALUE="${BROWSER:-chrome}"
                    BROWSER_VERSION_VALUE="${BROWSER_VERSION:-128.0}"
                    THREADS_VALUE="${THREADS:-1}"
                    EXECUTOR_URL_VALUE="${EXECUTOR_URL:-http://selenoid:4444/wd/hub}"
                    BASE_URL_VALUE="${BASE_URL:-http://prestashop:80/}"

                    echo "BROWSER=${BROWSER_VALUE}"
                    echo "BROWSER_VERSION=${BROWSER_VERSION_VALUE}"
                    echo "THREADS=${THREADS_VALUE}"
                    echo "EXECUTOR_URL=${EXECUTOR_URL_VALUE}"
                    echo "BASE_URL=${BASE_URL_VALUE}"

                    if [ "${THREADS_VALUE}" = "1" ]; then
                        docker run --name pytest_runner \
                            --network app_network \
                            -e BASE_URL="${BASE_URL_VALUE}" \
                            ${COMPOSE_PROJECT_NAME}-tests:latest \
                            tests/ \
                            -v \
                            --browser="${BROWSER_VALUE}" \
                            --browser_version="${BROWSER_VERSION_VALUE}" \
                            --executor="${EXECUTOR_URL_VALUE}" \
                            --base-url="${BASE_URL_VALUE}" \
                            --alluredir=/app/allure-results

                        TEST_EXIT_CODE=$?
                    else
                        docker run --name pytest_runner \
                            --network app_network \
                            -e BASE_URL="${BASE_URL_VALUE}" \
                            ${COMPOSE_PROJECT_NAME}-tests:latest \
                            tests/ \
                            -v \
                            --browser="${BROWSER_VALUE}" \
                            --browser_version="${BROWSER_VERSION_VALUE}" \
                            --executor="${EXECUTOR_URL_VALUE}" \
                            --base-url="${BASE_URL_VALUE}" \
                            --alluredir=/app/allure-results \
                            -n "${THREADS_VALUE}"

                        TEST_EXIT_CODE=$?
                    fi

                    echo "Test exit code: ${TEST_EXIT_CODE}"
                    exit ${TEST_EXIT_CODE}
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "Extracting reports and logs..."

                mkdir -p allure-results
                mkdir -p build-logs

                docker ps -a > build-logs/docker-ps.log || true
                docker logs prestashop > build-logs/prestashop.log 2>&1 || true
                docker logs selenoid > build-logs/selenoid.log 2>&1 || true
                docker logs pytest_runner > build-logs/pytest_runner.log 2>&1 || true

                docker cp pytest_runner:/app/allure-results/. allure-results/ || true

                echo "Cleaning up..."
                docker compose --profile tests --profile prestashop down -v --remove-orphans || true
                docker rm -f pytest_runner 2>/dev/null || true
            '''

            archiveArtifacts artifacts: 'build-logs/**', allowEmptyArchive: true
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true

            allure([
                includeProperties: false,
                jdk: '',
                commandline: 'Allure',
                results: [[path: 'allure-results']]
            ])
        }
    }
}