# 持续集成与持续测试
## 本章学习目标
- 理解持续集成（CI）和持续测试的概念
- 掌握主流CI/CD工具的使用（Jenkins、GitLab CI、GitHub Actions）
- 学会编写自动化测试流水线
- 了解测试左移和测试右移实践
- 构建完整的持续测试体系

---

## 1. 持续集成与持续测试概述
### 1.1 基本概念
```
CI/CD 流程：
├── 持续集成 (CI)
│   ├── 代码提交
│   ├── 自动构建
│   ├── 单元测试
│   └── 代码质量检查
├── 持续交付 (CD)
│   ├── 集成测试
│   ├── 部署到测试环境
│   └── 自动化测试
└── 持续部署 (CD)
    ├── 预发布验证
    ├── 生产部署
    └── 监控和回滚
```

### 1.2 持续测试的价值
```text
# 持续测试的优势
benefits = {
    "快速反馈": {
        "description": "代码提交后立即发现问题",
        "time_saving": "从小时级到分钟级",
        "example": "单元测试在5分钟内完成"
    },
    "质量保障": {
        "description": "每次提交都经过测试",
        "metrics": [
            "缺陷逃逸率降低50%",
            "代码覆盖率提升",
            "回归缺陷减少"
        ]
    },
    "效率提升": {
        "description": "自动化替代手动测试",
        "improvement": [
            "测试执行时间减少80%",
            "测试人员专注探索性测试",
            "减少重复劳动"
        ]
    },
    "风险降低": {
        "description": "早期发现问题，降低修复成本",
        "cost_ratio": "开发阶段:1 → 生产阶段:100"
    },
    "团队协作": {
        "description": "标准化流程，提高协作效率",
        "practices": [
            "测试即代码",
            "文档自动化",
            "知识共享"
        ]
    }
}
```

### 1.3 持续测试成熟度模型
```
成熟度等级：
├── Level 1: 手动测试
│   └── 无自动化，发布前手动测试
├── Level 2: 自动化单元测试
│   └── 有单元测试，但不持续运行
├── Level 3: 持续集成
│   └── 提交触发测试，快速反馈
├── Level 4: 持续测试
│   └── 全自动化测试套件，多环境验证
└── Level 5: 智能测试
    └── AI辅助，精准测试，自愈系统
```

---

## 2. Jenkins 持续集成
### 2.1 Jenkins 安装和配置
```bash
# Docker方式安装Jenkins
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts-jdk11

# 初始密码
docker logs jenkins

# 访问 http://localhost:8080
# 输入初始密码
# 安装推荐插件
# 创建管理员账号
```

### 2.2 Jenkins Pipeline 基础
```python
// Jenkinsfile - 基础流水线
pipeline {
    agent any

    stages {
        stage('检出代码') {
            steps {
                checkout scm
            }
        }

        stage('依赖安装') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install -r requirements-test.txt'
            }
        }

        stage('单元测试') {
            steps {
                sh 'pytest tests/unit --cov=app --cov-report=xml'
            }
            post {
                always {
                    junit 'test-reports/*.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        stage('代码质量检查') {
            steps {
                sh 'flake8 app/'
                sh 'pylint app/'
            }
        }

        stage('构建镜像') {
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
            }
        }

        stage('部署测试环境') {
            steps {
                sh 'docker-compose -f docker-compose.test.yml up -d'
            }
        }

        stage('集成测试') {
            steps {
                sh 'pytest tests/integration'
            }
        }
    }

    post {
        success {
            echo '流水线成功'
            emailext (
                subject: "SUCCESS: Job ${env.JOB_NAME}",
                body: "构建成功: ${env.BUILD_URL}",
                to: "team@example.com"
            )
        }
        failure {
            echo '流水线失败'
            emailext (
                subject: "FAILED: Job ${env.JOB_NAME}",
                body: "构建失败: ${env.BUILD_URL}",
                to: "team@example.com"
            )
        }
    }
}
```

### 2.3 多阶段流水线
```python
// 完整的CI/CD流水线
pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        APP_NAME = 'ecommerce-api'
        VERSION = "${BUILD_NUMBER}"
    }

    stages {
        // 阶段1: 代码检出和验证
        stage('准备') {
            steps {
                checkout scm
                script {
                    // 获取Git信息
                    COMMIT_HASH = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    COMMIT_AUTHOR = sh(
                        script: 'git log --format="%an" -n 1',
                        returnStdout: true
                    ).trim()
                }
                echo "构建版本: ${VERSION}, 提交: ${COMMIT_HASH}, 作者: ${COMMIT_AUTHOR}"
            }
        }

        // 阶段2: 依赖安装和安全扫描
        stage('依赖检查') {
            parallel {
                stage('安装依赖') {
                    steps {
                        sh '''
                            pip install -r requirements.txt
                            pip install -r requirements-test.txt
                        '''
                    }
                }
                stage('安全扫描') {
                    steps {
                        sh 'pip install safety'
                        sh 'safety check --json --output safety-report.json'
                    }
                    post {
                        always {
                            publishHTML([
                                reportDir: '.',
                                reportFiles: 'safety-report.json',
                                reportName: 'Security Scan'
                            ])
                        }
                    }
                }
            }
        }

        // 阶段3: 单元测试和覆盖率
        stage('单元测试') {
            steps {
                sh '''
                    pytest tests/unit \
                        --cov=app \
                        --cov-report=xml \
                        --cov-report=html \
                        --junitxml=test-reports/unit.xml
                '''
            }
            post {
                always {
                    junit 'test-reports/unit.xml'
                    publishHTML([
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                    // 上传覆盖率到SonarQube
                    withSonarQubeEnv('sonar-server') {
                        sh 'sonar-scanner'
                    }
                }
            }
        }

        // 阶段4: 集成测试
        stage('集成测试') {
            steps {
                // 启动测试环境
                sh 'docker-compose -f docker-compose.test.yml up -d'

                // 等待服务就绪
                sh 'sleep 10'

                // 运行集成测试
                sh '''
                    pytest tests/integration \
                        --junitxml=test-reports/integration.xml
                '''
            }
            post {
                always {
                    junit 'test-reports/integration.xml'
                    sh 'docker-compose -f docker-compose.test.yml down'
                }
            }
        }

        // 阶段5: API测试
        stage('API测试') {
            steps {
                sh 'docker-compose -f docker-compose.test.yml up -d'
                sh 'sleep 5'
                sh '''
                    docker run --rm \
                        --network=host \
                        -v $(pwd)/tests/api:/etc/newman \
                        postman/newman run collection.json \
                        --reporters=cli,html \
                        --reporter-html-export=api-report.html
                '''
            }
            post {
                always {
                    publishHTML([
                        reportDir: '.',
                        reportFiles: 'api-report.html',
                        reportName: 'API Test Report'
                    ])
                    sh 'docker-compose -f docker-compose.test.yml down'
                }
            }
        }

        // 阶段6: 性能测试
        stage('性能测试') {
            steps {
                sh 'docker-compose -f docker-compose.test.yml up -d'
                sh 'sleep 5'
                sh '''
                    docker run --rm \
                        --network=host \
                        -v $(pwd)/tests/perf:/scripts \
                        loadimpact/k6 run /scripts/load_test.js \
                        --out influxdb=http://localhost:8086/k6
                '''
            }
            post {
                always {
                    sh 'docker-compose -f docker-compose.test.yml down'
                }
            }
        }

        // 阶段7: 代码质量检查
        stage('代码质量') {
            parallel {
                stage('静态分析') {
                    steps {
                        sh '''
                            flake8 app/ --output-file=flake8-report.txt
                            pylint app/ --output-format=pylint2json > pylint-report.json
                        '''
                    }
                    post {
                        always {
                            publishHTML([
                                reportDir: '.',
                                reportFiles: 'flake8-report.txt',
                                reportName: 'Flake8 Report'
                            ])
                        }
                    }
                }
                stage('安全扫描') {
                    steps {
                        sh '''
                            bandit -r app/ -f json -o bandit-report.json
                        '''
                    }
                    post {
                        always {
                            publishHTML([
                                reportDir: '.',
                                reportFiles: 'bandit-report.json',
                                reportName: 'Security Report'
                            ])
                        }
                    }
                }
            }
        }

        // 阶段8: 构建和推送镜像
        stage('构建镜像') {
            steps {
                script {
                    // 多环境镜像
                    def images = [
                        "${DOCKER_REGISTRY}/${APP_NAME}:${VERSION}",
                        "${DOCKER_REGISTRY}/${APP_NAME}:latest"
                    ]

                    images.each { image ->
                        sh "docker build -t ${image} ."
                        sh "docker push ${image}"
                    }
                }
            }
        }

        // 阶段9: 部署到测试环境
        stage('部署测试') {
            steps {
                sh '''
                    docker-compose -f docker-compose.test.yml pull
                    docker-compose -f docker-compose.test.yml up -d
                '''
            }
        }

        // 阶段10: 验证部署
        stage('部署验证') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://localhost:5000/health || exit 1
                    curl -f http://localhost:5000/api/users || exit 1
                '''
            }
        }

        // 阶段11: 生成报告
        stage('生成报告') {
            steps {
                sh '''
                    # 合并所有测试报告
                    python scripts/merge_reports.py
                '''
                publishHTML([
                    reportDir: 'reports',
                    reportFiles: 'index.html',
                    reportName: 'Test Summary Report'
                ])
            }
        }

        // 阶段12: 部署到预发布
        stage('部署预发布') {
            when {
                branch 'main'
            }
            steps {
                input message: '部署到预发布环境？', ok: '部署'

                sh '''
                    docker-compose -f docker-compose.staging.yml up -d
                '''
            }
        }
    }

    post {
        always {
            // 清理工作空间
            cleanWs()

            // 发送通知
            script {
                def status = currentBuild.currentResult
                def color = status == 'SUCCESS' ? 'good' : 'danger'
                def emoji = status == 'SUCCESS' ? '✅' : '❌'

                // Slack通知
                slackSend(
                    channel: '#ci-cd',
                    color: color,
                    message: "${emoji} ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${status}\n${env.BUILD_URL}"
                )
            }
        }

        success {
            echo '流水线执行成功'
        }

        failure {
            echo '流水线执行失败'
        }

        unstable {
            echo '流水线执行不稳定'
        }
    }
}
```

---

## 3. GitLab CI/CD
### 3.1 GitLab CI 基础配置
```text
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_REGISTRY: registry.example.com
  APP_NAME: ecommerce-api
  DOCKER_DRIVER: overlay2

# 缓存配置
cache:
  paths:
    - .cache/pip
    - venv/

# 单元测试
unit_test:
  stage: test
  image: python:3.9-slim
  before_script:
    - pip install -r requirements.txt
    - pip install -r requirements-test.txt
  script:
    - pytest tests/unit --cov=app --cov-report=xml --junitxml=unit.xml
  artifacts:
    reports:
      junit: unit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - htmlcov/
    expire_in: 1 week
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  only:
    - merge_requests
    - main
    - develop

# 集成测试
integration_test:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_TLS_CERTDIR: ""
  before_script:
    - docker info
  script:
    - docker-compose -f docker-compose.test.yml up -d
    - sleep 10
    - pip install pytest requests
    - pytest tests/integration --junitxml=integration.xml
  artifacts:
    reports:
      junit: integration.xml
    paths:
      - logs/
    expire_in: 1 week
  after_script:
    - docker-compose -f docker-compose.test.yml down
  only:
    - merge_requests
    - main

# API测试
api_test:
  stage: test
  image: postman/newman
  script:
    - newman run tests/api/collection.json --reporters=cli,html --reporter-html-export=api-report.html
  artifacts:
    paths:
      - api-report.html
    expire_in: 1 week
  only:
    - main

# 性能测试
performance_test:
  stage: test
  image: loadimpact/k6
  script:
    - k6 run tests/perf/load_test.js
  only:
    - schedules
  when: manual

# 代码质量检查
code_quality:
  stage: test
  image: python:3.9-slim
  before_script:
    - pip install flake8 pylint bandit
  script:
    - flake8 app/ --output-file=flake8.txt
    - pylint app/ --output-format=pylint2json > pylint.json
    - bandit -r app/ -f json -o bandit.json
  artifacts:
    paths:
      - flake8.txt
      - pylint.json
      - bandit.json
    expire_in: 1 week
  only:
    - merge_requests

# 构建镜像
build_image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_TLS_CERTDIR: ""
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main

# 部署测试环境
deploy_test:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_TLS_CERTDIR: ""
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker-compose -f docker-compose.test.yml pull
    - docker-compose -f docker-compose.test.yml up -d
  environment:
    name: test
    url: http://test.example.com
  only:
    - main

# 部署预发布
deploy_staging:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_TLS_CERTDIR: ""
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker-compose -f docker-compose.staging.yml pull
    - docker-compose -f docker-compose.staging.yml up -d
  environment:
    name: staging
    url: http://staging.example.com
  when: manual
  only:
    - main

# 生成测试报告
test_report:
  stage: test
  image: python:3.9-slim
  script:
    - pip install pytest-html
    - pytest --html=report.html --self-contained-html
  artifacts:
    paths:
      - report.html
    expire_in: 1 week
  only:
    - main

# 通知
notify:
  stage: test
  image: alpine:latest
  script:
    - apk add curl
    - |
      curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"构建完成: '"$CI_PROJECT_NAME"' - '"$CI_COMMIT_SHA"'"}' \
        $SLACK_WEBHOOK_URL
  when: on_success
  only:
    - main
```

### 3.2 GitLab CI 高级配置
```text
# .gitlab-ci.yml - 高级版
include:
  - template: Jobs/Code-Quality.gitlab-ci.yml
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Dependency-Scanning.gitlab-ci.yml
  - template: Jobs/Container-Scanning.gitlab-ci.yml

stages:
  - validate
  - test
  - build
  - security
  - deploy
  - monitor

# 验证阶段
validate_code:
  stage: validate
  image: python:3.9-slim
  script:
    - pip install black isort
    - black --check app/
    - isort --check-only app/
  only:
    - merge_requests

# 单元测试矩阵
unit_test_matrix:
  stage: test
  image: python:${PYTHON_VERSION}
  parallel:
    matrix:
      - PYTHON_VERSION: ['3.8', '3.9', '3.10']
  script:
    - pip install -r requirements.txt -r requirements-test.txt
    - pytest tests/unit --cov=app
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

# 集成测试（带服务）
integration_test:
  stage: test
  image: python:3.9-slim
  services:
    - name: postgres:13
      alias: db
      variables:
        POSTGRES_DB: testdb
        POSTGRES_USER: test
        POSTGRES_PASSWORD: test
    - name: redis:6
      alias: redis
  variables:
    DB_HOST: db
    REDIS_HOST: redis
  before_script:
    - pip install -r requirements.txt
    - python scripts/wait_for_services.py
  script:
    - pytest tests/integration
  artifacts:
    reports:
      junit: integration.xml
    paths:
      - logs/

# 安全扫描
security_scan:
  stage: security
  image: owasp/zap2docker-stable
  script:
    - zap-baseline.py -t http://test.example.com
  artifacts:
    paths:
      - zap-report.html
  only:
    - main

# 构建多架构镜像
build_multi_arch:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker buildx create --use
    - docker buildx build \
        --platform linux/amd64,linux/arm64 \
        -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA \
        -t $CI_REGISTRY_IMAGE:latest \
        --push .
  only:
    - main

# 蓝绿部署
deploy_blue_green:
  stage: deploy
  image: alpine:latest
  script:
    # 切换流量到新版本
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    # 等待就绪
    - kubectl rollout status deployment/app
    # 如果失败自动回滚
    - kubectl rollout undo deployment/app || true
  environment:
    name: production
    url: https://app.example.com
  when: manual
  only:
    - main

# 性能测试
performance_test:
  stage: monitor
  image: loadimpact/k6
  script:
    - k6 run --out influxdb=http://influxdb:8086/k6 tests/perf/load_test.js
  artifacts:
    paths:
      - k6-results.html
  only:
    - schedules
  when: manual

# 监控告警
monitoring:
  stage: monitor
  image: alpine:latest
  script:
    - apk add curl jq
    - |
      # 检查应用健康
      STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://app:5000/health)
      if [ "$STATUS" != "200" ]; then
        curl -X POST $ALERT_WEBHOOK -d '{"alert":"应用健康检查失败"}'
        exit 1
      fi
  only:
    - main
```

---

## 4. GitHub Actions
### 4.1 基础工作流
```text
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # 单元测试
  test:
    runs-on: ubuntu-latest

    steps:
    - name: 检出代码
      uses: actions/checkout@v3

    - name: 设置Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        cache: 'pip'

    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: 运行单元测试
      run: |
        pytest tests/unit --cov=app --cov-report=xml --junitxml=unit.xml

    - name: 上传测试报告
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: |
          unit.xml
          htmlcov/
        retention-days: 7

    - name: 上传覆盖率到Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  # 集成测试
  integration-test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:6
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3

    - name: 设置Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: 安装依赖
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: 等待服务就绪
      run: |
        chmod +x scripts/wait_for_services.sh
        ./scripts/wait_for_services.sh

    - name: 运行集成测试
      env:
        DB_HOST: localhost
        REDIS_HOST: localhost
      run: |
        pytest tests/integration --junitxml=integration.xml

    - name: 上传集成测试报告
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: integration-results
        path: integration.xml
        retention-days: 7

  # 代码质量检查
  code-quality:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: 设置Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: 安装检查工具
      run: |
        pip install flake8 pylint bandit black isort

    - name: 代码风格检查
      run: |
        black --check app/
        isort --check-only app/

    - name: Lint检查
      run: |
        flake8 app/ --output-file=flake8.txt
        pylint app/ --output-format=pylint2json > pylint.json

    - name: 安全扫描
      run: |
        bandit -r app/ -f json -o bandit.json

    - name: 上传报告
      uses: actions/upload-artifact@v3
      with:
        name: quality-reports
        path: |
          flake8.txt
          pylint.json
          bandit.json
        retention-days: 7

  # 构建和推送镜像
  build-and-push:
    runs-on: ubuntu-latest

    needs: [test, integration-test, code-quality]

    if: github.ref == 'refs/heads/main'

    permissions:
      contents: read
      packages: write

    steps:
    - uses: actions/checkout@v3

    - name: 设置Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: 登录GitHub Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: 提取元数据
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}

    - name: 构建并推送
      uses: docker/build-push-action@v4
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  # 部署到测试环境
  deploy-test:
    runs-on: ubuntu-latest

    needs: build-and-push

    if: github.ref == 'refs/heads/main'

    environment:
      name: test
      url: https://test.example.com

    steps:
    - uses: actions/checkout@v3

    - name: 设置Kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.27.0'

    - name: 配置Kubernetes访问
      run: |
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig

    - name: 部署到测试环境
      run: |
        kubectl set image deployment/app app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} -n test
        kubectl rollout status deployment/app -n test --timeout=300s

    - name: 验证部署
      run: |
        kubectl get pods -n test
        curl -f https://test.example.com/health

  # 部署到预发布环境
  deploy-staging:
    runs-on: ubuntu-latest

    needs: deploy-test-test-if

 ref

 if
 if if


 on













 approval



,






name环境







-st environment环境 environment environment
/:







- name production
st
 environment


 environment

 environmenting


 production
 environment
-st


 production-st production-st
 {
.sh

 deployment-st

-st to

 environment:
 secrets-st run

::
:
 environment
 secrets
 ** manually and.sh to




:

      run: |
        kubectl set image deployment/app app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} -n staging
        kubectl rollout status deployment/app -n staging --timeout=300s

    - name: 运行冒烟测试
      run: |
        pytest tests/smoke --env=staging

    - name: 手动确认
      uses: hmarr/auto-approve-action@v3
      with:
        github-token: ${{ secrets.GITHUB_TOKEN }}

  # 部署到生产环境
  deploy-production:
    runs-on: ubuntu-latest

    needs: deploy-staging

    if: github.ref == 'refs/heads/main'

    environment:
      name: production
      url: https://app.example.com

    steps:
    - uses: actions/checkout@v3

    - name: 设置Kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.27.0'

    - name: 配置Kubernetes访问
      run: |
        echo "${{ secrets.KUBE_CONFIG_PROD }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig

    - name: 蓝绿部署
      run: |
        # 创建新版本
        kubectl set image deployment/app app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} -n production

        # 等待就绪
        kubectl rollout status deployment/app -n production --timeout=600s

        # 健康检查
        curl -f https://app.example.com/health

        # 如果失败自动回滚
        if [ $? -ne 0 ]; then
          kubectl rollout undo deployment/app -n production
          exit 1
        fi

    - name: 发送通知
      if: always()
      run: |
        curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
          -H 'Content-type: application/json' \
          --data '{"text":"生产部署完成: '"${{ github.repository }}"' - '"${{ github.sha }}"'"}'

  # 性能测试
  performance-test:
    runs-on: ubuntu-latest

    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'

    steps:
    - uses: actions/checkout@v3

    - name: 运行性能测试
      uses: loadimpact/k6-action@v1
      with:
        filename: tests/perf/load_test.js
        flags: --out influxdb=http://influxdb:8086/k6

    - name: 上传测试报告
      uses: actions/upload-artifact@v3
      with:
        name: performance-results
        path: k6-results.html
        retention-days: 30

  # 安全扫描
  security-scan:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: 运行Trivy扫描
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: '${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: 上传到GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: trivy-results.sarif

  # 生成测试报告
  test-report:
    runs-on: ubuntu-latest

    needs: [test, integration-test]

    if: always()

    steps:
    - uses: actions/checkout@v3

    - name: 下载所有测试报告
      uses: actions/download-artifact@v3

    - name: 生成汇总报告
      run: |
        python scripts/generate_report.py \
          --unit-test test-results/unit.xml \
          --integration-test integration-results/integration.xml \
          --output report.html

    - name: 上传报告
      uses: actions/upload-artifact@v3
      with:
        name: test-report
        path: report.html
        retention-days: 30

    - name: 评论PR
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = fs.readFileSync('report.html', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `## 测试报告\n\n${report}`
          });
```

### 4.2 高级工作流模式
```text
# .github/workflows/advanced.yml
name: Advanced CI/CD

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'app/**'
      - 'tests/**'
      - '.github/workflows/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'app/**'
      - 'tests/**'

# 环境变量
env:
  PYTHON_VERSION: '3.9'
  DOCKER_REGISTRY: ghcr.io
  APP_NAME: ${{ github.repository }}

jobs:
  # 变更检测
  changes:
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.filter.outputs.backend }}
      frontend: ${{ steps.filter.outputs.frontend }}
      tests: ${{ steps.filter.outputs.tests }}
    steps:
    - uses: actions/checkout@v3
    - uses: dorny/paths-filter@v2
      id: filter
      with:
        filters: |
          backend:
            - 'app/backend/**'
            - 'requirements.txt'
          frontend:
            - 'app/frontend/**'
            - 'package.json'
          tests:
            - 'tests/**'

  # 并行测试
  test-matrix:
    runs-on: ubuntu-latest
    needs: changes
    if: needs.changes.outputs.tests == 'true'

    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10']
        test-group: ['unit', 'integration', 'e2e']

    steps:
    - uses: actions/checkout@v3

    - name: 设置Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'

    - name: 安装依赖
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: 运行测试
      run: |
        pytest tests/${{ matrix.test-group }} \
          --cov=app \
          --cov-report=xml:${{ matrix.test-group }}-coverage.xml \
          --junitxml=${{ matrix.test-group }}-results.xml

    - name: 上传结果
      uses: actions/upload-artifact@v3
      with:
        name: test-${{ matrix.python-version }}-${{ matrix.test-group }}
        path: |
          ${{ matrix.test-group }}-results.xml
          ${{ matrix.test-group }}-coverage.xml
        retention-days: 7

  # 测试聚合
  test-summary:
    runs-on: ubuntu-latest
    needs: test-matrix
    if: always()

    steps:
    - uses: actions/checkout@v3

    - name: 下载所有测试结果
      uses: actions/download-artifact@v3

    - name: 汇总测试结果
      run: |
        python scripts/aggregate_tests.py \
          --input-dir . \
          --output summary.xml

    - name: 上传汇总报告
      uses: actions/upload-artifact@v3
      with:
        name: test-summary
        path: summary.xml
        retention-days: 30

  # 构建优化
  build:
    runs-on: ubuntu-latest
    needs: [changes, test-summary]
    if: needs.changes.outputs.backend == 'true' || needs.changes.outputs.frontend == 'true'

    steps:
    - uses: actions/checkout@v3

    - name: 设置Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: 登录容器注册表
      uses: docker/login-action@v2
      with:
        registry: ${{ env.DOCKER_REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: 构建后端
      if: needs.changes.outputs.backend == 'true'
      uses: docker/build-push-action@v4
      with:
        context: ./app/backend
        push: true
        tags: |
          ${{ env.DOCKER_REGISTRY }}/${{ env.APP_NAME }}/backend:${{ github.sha }}
          ${{ env.DOCKER_REGISTRY }}/${{ env.APP_NAME }}/backend:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
        platforms: linux/amd64,linux/arm64

    - name: 构建前端
      if: needs.changes.outputs.frontend == 'true'
      uses: docker/build-push-action@v4
      with:
        context: ./app/frontend
        push: true
        tags: |
          ${{ env.DOCKER_REGISTRY }}/${{ env.APP_NAME }}/frontend:${{ github.sha }}
          ${{ env.DOCKER_REGISTRY }}/${{ env.APP_NAME }}/frontend:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
        platforms: linux/amd64,linux/arm64

  # 部署到测试环境
  deploy-test:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'

    environment:
      name: test
      url: https://test.example.com

    steps:
    - uses: actions/checkout@v3

    - name: 部署
      uses: appleboy/ssh-action@v1.0.0
      with:
        host: ${{ secrets.TEST_SERVER_HOST }}
        username: ${{ secrets.TEST_SERVER_USER }}
        key: ${{ secrets.TEST_SSH_KEY }}
        script: |
          cd /opt/app/test
          docker-compose pull
          docker-compose up -d
          docker system prune -f

  # 部署到生产环境（带审批）
  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'

    environment:
      name: production
      url: https://app.example.com
      deployment-branch: main

    steps:
    - uses: actions/checkout@v3

    - name: 等待审批
      run: echo "等待环境审批..."

    - name: 部署到生产
      uses: appleboy/ssh-action@v1.0.0
      with:
        host: ${{ secrets.PROD_SERVER_HOST }}
        username: ${{ secrets.PROD_SERVER_USER }}
        key: ${{ secrets.PROD_SSH_KEY }}
        script: |
          cd /opt/app/prod
          # 蓝绿部署
          docker-compose -f docker-compose.blue.yml up -d
          sleep 30
          # 健康检查
          if curl -f http://localhost:5000/health; then
            docker-compose -f docker-compose.green.yml down
          else
            docker-compose -f docker-compose.blue.yml down
            exit 1
          fi

  # 通知
  notify:
    runs-on: ubuntu-latest
    needs: [deploy-test, deploy-production]
    if: always()

    steps:
    - name: 发送通知
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        channel: '#ci-cd'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        fields: repo,message,commit,author,action,eventName,ref,workflow
```

---

## 5. 测试左移与测试右移
### 5.1 测试左移（Shift Left）
```python
# pre_commit_hook.py
#!/usr/bin/env python3

"""
Git预提交钩子 - 测试左移实践
"""

import subprocess
import sys
import os

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_code_quality():
    """代码质量检查"""
    print("🔍 检查代码质量...")

    # 代码格式化
    success, output = run_command("black --check app/ tests/")
    if not success:
        print("❌ 代码格式不符合规范")
        print(output)
        return False

    # 导入排序
    success, output = run_command("isort --check-only app/ tests/")
    if not success:
        print("❌ 导入顺序需要调整")
        print(output)
        return False

    # Lint检查
    success, output = run_command("flake8 app/ tests/")
    if not success:
        print("❌ 代码质量问题")
        print(output)
        return False

    print("✅ 代码质量检查通过")
    return True

def run_unit_tests():
    """运行单元测试"""
    print("🧪 运行单元测试...")

    success, output = run_command(
        "pytest tests/unit -v --tb=short --no-header -q"
    )

    if not success:
        print("❌ 单元测试失败")
        print(output)
        return False

    print("✅ 单元测试通过")
    return True

def check_security():
    """安全检查"""
    print("🔒 运行安全扫描...")

    success, output = run_command("bandit -r app/ -f json")
    if not success:
        print("⚠️  发现安全问题")
        print(output)
        # 不阻塞提交，只警告

    print("✅ 安全检查完成")
    return True

def check_dependencies():
    """依赖安全检查"""
    print("📦 检查依赖安全...")

    success, output = run_command("safety check --json")
    if not success:
        print("⚠️  发现不安全的依赖")
        print(output)
        # 可配置为阻塞或警告

    print("✅ 依赖检查完成")
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("预提交检查开始")
    print("=" * 50)

    checks = [
        ("代码质量", check_code_quality),
        ("单元测试", run_unit_tests),
        ("安全扫描", check_security),
        ("依赖检查", check_dependencies),
    ]

    failed = []

    for name, check_func in checks:
        print(f"\n{name}...")
        if not check_func():
            failed.append(name)

    print("\n" + "=" * 50)
    if failed:
        print(f"❌ 检查失败: {', '.join(failed)}")
        print("提交被拒绝，请修复问题后重试")
        sys.exit(1)
    else:
        print("✅ 所有检查通过，允许提交")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### 5.2 测试右移（Shift Right）
```python
# production_monitoring.py
"""
生产环境监控和测试
"""

import requests
import logging
from datetime import datetime
import json

class ProductionMonitor:
    """生产环境监控器"""

    def __init__(self, base_url, alert_webhook=None):
        self.base_url = base_url
        self.alert_webhook = alert_webhook
        self.logger = logging.getLogger(__name__)

    def health_check(self):
        """健康检查"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"健康检查失败: {e}")
            return False

    def smoke_test(self):
        """冒烟测试"""
        test_cases = [
            ("/api/users", "GET", 200),
            ("/api/products", "GET", 200),
            ("/api/health", "GET", 200),
        ]

        results = []

        for endpoint, method, expected_status in test_cases:
            try:
                response = requests.request(
                    method,
                    f"{self.base_url}{endpoint}",
                    timeout=5
                )
                success = response.status_code == expected_status
                results.append({
                    "endpoint": endpoint,
                    "method": method,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "success": success
                })

                if not success:
                    self.logger.warning(
                        f"冒烟测试失败: {endpoint} - "
                        f"期望 {expected_status}, 实际 {response.status_code}"
                    )
            except Exception as e:
                results.append({
                    "endpoint": endpoint,
                    "method": method,
                    "error": str(e),
                    "success": False
                })
                self.logger.error(f"冒烟测试异常: {endpoint} - {e}")

        return results

    def canary_analysis(self, canary_id):
        """金丝雀分析"""
        # 获取金丝雀指标
        metrics = self.get_metrics(canary_id)

        # 对比基线
        baseline = self.get_baseline_metrics()

        analysis = {
            "latency": self.compare_latency(metrics, baseline),
            "error_rate": self.compare_error_rate(metrics, baseline),
            "throughput": self.compare_throughput(metrics, baseline)
        }

        return analysis

    def get_metrics(self, canary_id):
        """获取指标"""
        # 从监控系统获取指标
        return {
            "latency": 150,  # ms
            "error_rate": 0.01,  # 1%
            "throughput": 1000  # req/s
        }

    def get_baseline_metrics(self):
        """获取基线指标"""
        return {
            "latency": 100,
            "error_rate": 0.005,
            "throughput": 1200
        }

    def compare_latency(self, metrics, baseline):
        """比较延迟"""
        current = metrics["latency"]
        base = baseline["latency"]
        threshold = base * 1.2  # 20%阈值

        return {
            "current": current,
            "baseline": base,
            "status": "pass" if current <= threshold else "fail",
            "ratio": current / base
        }

    def compare_error_rate(self, metrics, baseline):
        """比较错误率"""
        current = metrics["error_rate"]
        base = baseline["error_rate"]
        threshold = base * 2  # 错误率翻倍阈值

        return {
            "current": current,
            "baseline": base,
            "status": "pass" if current <= threshold else "fail",
            "ratio": current / base
        }

    def compare_throughput(self, metrics, baseline):
        """比较吞吐量"""
        current = metrics["throughput"]
        base = baseline["throughput"]
        threshold = base * 0.8  # 下降20%阈值

        return {
            "current": current,
            "baseline": base,
            "status": "pass" if current >= threshold else "fail",
            "ratio": current / base
        }

    def send_alert(self, message, severity="warning"):
        """发送告警"""
        if not self.alert_webhook:
            return

        payload = {
            "text": f"[{severity.upper()}] {message}",
            "timestamp": datetime.now().isoformat(),
            "service": "production-monitor"
        }

        try:
            requests.post(
                self.alert_webhook,
                json=payload,
                timeout=5
            )
        except Exception as e:
            self.logger.error(f"发送告警失败: {e}")

    def run_continuous_testing(self, interval=60):
        """持续测试"""
        import time

        self.logger.info("开始持续测试...")

        while True:
            try:
                # 健康检查
                if not self.health_check():
                    self.send_alert("健康检查失败", "critical")

                # 冒烟测试
                smoke_results = self.smoke_test()
                failed = [r for r in smoke_results if not r["success"]]

                if failed:
                    self.send_alert(
                        f"冒烟测试失败: {len(failed)}个测试",
                        "error"
                    )

                # 记录日志
                self.logger.info(
                    f"测试完成 - 成功: {len(smoke_results) - len(failed)}, "
                    f"失败: {len(failed)}"
                )

                time.sleep(interval)

            except KeyboardInterrupt:
                self.logger.info("持续测试停止")
                break
            except Exception as e:
                self.logger.error(f"持续测试异常: {e}")
                time.sleep(interval)

# 使用示例
if __name__ == "__main__":
    monitor = ProductionMonitor(
        base_url="https://app.example.com",
        alert_webhook="https://hooks.slack.com/services/YOUR/WEBHOOK"
    )

    # 一次性测试
    print("运行冒烟测试...")
    results = monitor.smoke_test()
    print(json.dumps(results, indent=2))

    # 持续测试
    # monitor.run_continuous_testing(interval=300)
```

---

## 6. 实践案例：完整CI/CD流水线
### 6.1 项目结构
```
project/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── nightly.yml
├── app/
│   ├── backend/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── frontend/
│       ├── package.json
│       └── Dockerfile
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   └── perf/
├── docker-compose.yml
├── Jenkinsfile
├── .gitlab-ci.yml
└── scripts/
    ├── deploy.sh
    ├── test.sh
    └── monitor.sh
```

### 6.2 完整流水线实现
```python
#!/bin/bash
# scripts/ci-cd-pipeline.sh
set -e

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 阶段1: 代码质量检查
code_quality_check() {
    log_info "阶段1: 代码质量检查"

    # 代码格式化
    log_info "检查代码格式..."
    black --check app/ tests/

    # 导入排序
    log_info "检查导入顺序..."
    isort --check-only app/ tests/

    # Lint检查
    log_info "运行Lint检查..."
    flake8 app/ tests/

    # 类型检查
    log_info "运行类型检查..."
    mypy app/

    log_info "✅ 代码质量检查通过"
}

# 阶段2: 单元测试
unit_tests() {
    log_info "阶段2: 单元测试"

    pytest tests/unit \
        --cov=app \
        --cov-report=xml \
        --cov-report=html \
        --cov-fail-under=80 \
        --junitxml=reports/unit.xml

    log_info "✅ 单元测试通过"
}

# 阶段3: 集成测试
integration_tests() {
    log_info "阶段3: 集成测试"

    # 启动测试环境
    log_info "启动测试环境..."
    docker-compose -f docker-compose.test.yml up -d

    # 等待服务就绪
    log_info "等待服务就绪..."
    ./scripts/wait_for_services.sh

    # 运行测试
    pytest tests/integration \
        --junitxml=reports/integration.xml

    # 清理
    docker-compose -f docker-compose.test.yml down

    log_info "✅ 集成测试通过"
}

# 阶段4: API测试
api_tests() {
    log_info "阶段4: API测试"

    # 启动服务
    docker-compose -f docker-compose.test.yml up -d

    # 运行API测试
    docker run --rm \
        --network=host \
        -v $(pwd)/tests/api:/etc/newman \
        postman/newman run collection.json \
        --reporters=cli,html \
        --reporter-html-export=reports/api.html

    docker-compose -f docker-compose.test.yml down

    log_info "✅ API测试通过"
}

# 阶段5: 性能测试
performance_tests() {
    log_info "阶段5: 性能测试"

    # 启动服务
    docker-compose -f docker-compose.test.yml up -d

    # 运行性能测试
    docker run --rm \
        --network=host \
        -v $(pwd)/tests/perf:/scripts \
        loadimpact/k6 run /scripts/load_test.js

    docker-compose -f docker-compose.test.yml down

    log_info "✅ 性能测试完成"
}

# 阶段6: 安全扫描
security_scan() {
    log_info "阶段6: 安全扫描"

    # 依赖扫描
    log_info "扫描依赖..."
    safety check --json > reports/safety.json

    # 代码安全扫描
    log_info "扫描代码安全..."
    bandit -r app/ -f json -o reports/bandit.json

    # 容器扫描
    log_info "扫描容器镜像..."
    docker build -t app:test .
    trivy image --format json -o reports/trivy.json app:test

    log_info "✅ 安全扫描完成"
}

# 阶段7: 构建镜像
build_images() {
    log_info "阶段7: 构建镜像"

    # 构建后端
    log_info "构建后端镜像..."
    docker build -t registry.example.com/app/backend:$VERSION ./app/backend
    docker push registry.example.com/app/backend:$VERSION

    # 构建前端
    log_info "构建前端镜像..."
    docker build -t registry.example.com/app/frontend:$VERSION ./app/frontend
    docker push registry.example.com/app/frontend:$VERSION

    log_info "✅ 镜像构建完成"
}

# 阶段8: 部署测试环境
deploy_test() {
    log_info "阶段8: 部署测试环境"

    # 更新部署
    kubectl set image deployment/app \
        backend=registry.example.com/app/backend:$VERSION \
        frontend=registry.example.com/app/frontend:$VERSION \
        -n test

    # 等待就绪
    kubectl rollout status deployment/app -n test --timeout=300s

    # 运行冒烟测试
    log_info "运行冒烟测试..."
    ./scripts/smoke_test.sh https://test.example.com

    log_info "✅ 测试环境部署完成"
}

# 阶段9: 部署预发布
deploy_staging() {
    log_info "阶段9: 部署预发布环境"

    # 需要手动确认
    read -p "部署到预发布环境? (y/N): " confirm
    if [[ $confirm != "y" ]]; then
        log_warn "部署取消"
        return 1
    fi

    # 蓝绿部署
    kubectl set image deployment/app \
        backend=registry.example.com/app/backend:$VERSION \
        frontend=registry.example.com/app/frontend:$VERSION \
        -n staging

    kubectl rollout status deployment/app -n staging --timeout=300s

    # 运行完整测试
    log_info "运行预发布测试..."
    pytest tests/e2e --env=staging

    log_info "✅ 预发布环境部署完成"
}

# 阶段10: 部署生产
deploy_production() {
    log_info "阶段10: 部署生产环境"

    # 需要审批
    read -p "部署到生产环境? (y/N): " confirm
    if [[ $confirm != "y" ]]; then
        log_warn "部署取消"
        return 1
    fi

    # 蓝绿部署
    log_info "开始蓝绿部署..."
    kubectl set image deployment/app \
        backend=registry.example.com/app/backend:$VERSION \
        frontend=registry.example.com/app/frontend:$VERSION \
        -n production

    # 等待就绪
    kubectl rollout status deployment/app -n production --timeout=600s

    # 健康检查
    log_info "运行健康检查..."
    if ! ./scripts/health_check.sh https://app.example.com; then
        log_error "健康检查失败，回滚..."
        kubectl rollout undo deployment/app -n production
        exit 1
    fi

    # 金丝雀分析
    log_info "运行金丝雀分析..."
    ./scripts/canary_analysis.sh

    log_info "✅ 生产环境部署完成"
}

# 主流程
main() {
    # 解析参数
    ACTION=${1:-all}
    VERSION=${2:-$(git rev-parse --short HEAD)}

    log_info "CI/CD流水线开始"
    log_info "版本: $VERSION"

    case $ACTION in
        "test")
            code_quality_check
            unit_tests
            integration_tests
            api_tests
            ;;
        "build")
            build_images
            ;;
        "deploy-test")
            deploy_test
            ;;
        "deploy-staging")
            deploy_staging
            ;;
        "deploy-prod")
            deploy_production
            ;;
        "all")
            code_quality_check
            unit_tests
            integration_tests
            api_tests
            security_scan
            build_images
            deploy_test
            ;;
        *)
            echo "用法: $0 {test|build|deploy-test|deploy-staging|deploy-prod|all} [version]"
            exit 1
            ;;
    esac

    log_info "CI/CD流水线完成"
}

main "$@"
```

### 6.3 生成测试报告
```python
# scripts/generate_report.py
import xml.etree.ElementTree as ET
import json
from datetime import datetime
import sys

def parse_junit_xml(xml_file):
    """解析JUnit XML"""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    results = {
        "tests": int(root.get("tests", 0)),
        "failures": int(root.get("failures", 0)),
        "errors": int(root.get("errors", 0)),
        "skipped": int(root.get("skipped", 0)),
        "time": float(root.get("time", 0))
    }

    results["passed"] = results["tests"] - results["failures"] - results["errors"] - results["skipped"]

    return results

def generate_html_report(unit_results, integration_results, output_file):
    """生成HTML报告"""

    total_tests = unit_results["tests"] + integration_results["tests"]
    total_passed = unit_results["passed"] + integration_results["passed"]
    total_failed = unit_results["failures"] + integration_results["failures"]

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>测试报告</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
            .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
            .card {{ background: white; border: 1px solid #ddd; padding: 15px; border-radius: 5px; flex: 1; }}
            .pass {{ color: #28a745; }}
            .fail {{ color: #dc3545; }}
            .details {{ margin-top: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #f8f9fa; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>测试报告</h1>
            <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>

        <div class="summary">
            <div class="card">
                <h3>总测试数</h3>
                <p style="font-size: 24px;">{total_tests}</p>
            </div>
            <div class="card">
                <h3>通过</h3>
                <p style="font-size: 24px; color: #28a745;">{total_passed}</p>
            </div>
            <div class="card">
                <h3>失败</h3>
                <p style="font-size: 24px; color: #dc3545;">{total_failed}</p>
            </div>
            <div class="card">
                <h3>通过率</h3>
                <p style="font-size: 24px; color: #007bff;">
                    {total_passed/total_tests*100:.1f}%
                </p>
            </div>
        </div>

        <div class="details">
            <h2>详细信息</h2>
            <table>
                <tr>
                    <th>测试类型</th>
                    <th>总数</th>
                    <th>通过</th>
                    <th>失败</th>
                    <th>错误</th>
                    <th>跳过</th>
                    <th>耗时(s)</th>
                </tr>
                <tr>
                    <td>单元测试</td>
                    <td>{unit_results['tests']}</td>
                    <td class="pass">{unit_results['passed']}</td>
                    <td class="fail">{unit_results['failures']}</td>
                    <td class="fail">{unit_results['errors']}</td>
                    <td>{unit_results['skipped']}</td>
                    <td>{unit_results['time']:.2f}</td>
                </tr>
                <tr>
                    <td>集成测试</td>
                    <td>{integration_results['tests']}</td>
                    <td class="pass">{integration_results['passed']}</td>
                    <td class="fail">{integration_results['failures']}</td>
                    <td class="fail">{integration_results['errors']}</td>
                    <td>{integration_results['skipped']}</td>
                    <td>{integration_results['time']:.2f}</td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """

    with open(output_file, 'w') as f:
        f.write(html)

def main():
    if len(sys.argv) < 4:
        print("用法: python generate_report.py <unit_xml> <integration_xml <output>")
        sys.exit(1)

    unit_file = sys.argv[1]
    integration_file = sys.argv[2]
    output_file = sys.argv[3]

    unit_results = parse_junit_xml(unit_file)
    integration_results = parse_junit_xml(integration_file)

    generate_html_report(unit_results, integration_results, output_file)
    print(f"报告已生成: {output_file}")

if __name__ == "__main__":
    main()
```

---

## 7. 练习题
### 理论题
1. **简述持续集成的核心原则**
   - 答案要点：频繁提交、自动化构建、快速反馈、主干开发

2. **比较Jenkins、GitLab CI和GitHub Actions的优缺点**
   - 答案要点：灵活性、易用性、集成度、成本

3. **什么是测试左移？有哪些实践？**
   - 答案要点：预提交检查、代码审查、单元测试、TDD

### 实践题
1. **为一个Python项目编写完整的Jenkins Pipeline**
   - 要求：包含代码检查、测试、构建、部署

2. **配置GitLab CI/CD流水线**
   - 要求：使用Docker构建，多阶段测试，部署到Kubernetes

3. **实现生产环境监控和自动回滚**
   - 要求：健康检查、金丝雀分析、自动回滚机制

---

## 8. 参考资料
### 官方文档
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

### 推荐工具
- **CI/CD**: Jenkins, GitLab CI, GitHub Actions, CircleCI
- **容器**: Docker, Kubernetes
- **监控**: Prometheus, Grafana, ELK
- **安全**: Trivy, Snyk, SonarQube

### 在线资源
- CI/CD Best Practices: https://continuousdelivery.com/
- DevOps Roadmap: https://roadmap.sh/devops
- Kubernetes Patterns: https://kubernetespatterns.com/

---

## 本章小结
本章详细介绍了持续集成与持续测试的理论和实践。重点掌握：
- CI/CD核心概念和原则
- Jenkins、GitLab CI、GitHub Actions的使用
- 测试左移和测试右移实践
- 完整的自动化流水线构建
- 生产环境监控和自动回滚

通过本章学习，您应该能够为项目构建完整的CI/CD流水线，实现高质量的持续交付。
