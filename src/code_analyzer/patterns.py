# Здесь определяются все шаблоны и регулярные выражения
import re

ENDPOINT_IGNORE_FILE_PATTERNS = [
    # тестовые и мок-файлы
    re.compile(r'\b__tests__\b', re.IGNORECASE),
    re.compile(r'\b__mocks__\b', re.IGNORECASE),
    re.compile(r'\btest(s|ing)?\b', re.IGNORECASE),
    re.compile(r'\.test\.(js|ts)x?$', re.IGNORECASE),
    re.compile(r'\.(spec|e2e)\.(js|ts)x?$', re.IGNORECASE),

    # типичные сборки / дистрибуции / зависимости
    re.compile(r'\bnode_modules\b'),
    re.compile(r'\bvendor\b'),
    re.compile(r'\bdist\b'),
    re.compile(r'\bbuild\b'),
    re.compile(r'\bcoverage\b'),
    re.compile(r'\b\.git\b'),
    re.compile(r'\b\.next\b'),      # Next.js
    re.compile(r'\b\.nuxt\b'),      # Nuxt.js
    re.compile(r'\bpublic\b'),      # статические
    re.compile(r'\bfixtures?\b'),   # фикстуры

    # конфиг-папки
    re.compile(r'\bconfig\b'),
    re.compile(r'\bconfigs?\b'),
    re.compile(r'\b\.circleci\b'),
    re.compile(r'\bjenkins\b', re.IGNORECASE),
]

ENDPOINT_PATTERNS = {
    "Java": [
        (re.compile(r'@(?:RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)\s*\(\s*["\']([^"\']+)["\']'), "Spring MVC"),
        (re.compile(r'@Path\(\s*["\']([^"\']+)["\']\)'),                                          "JAX-RS"),
        (re.compile(r'@Route\(\s*path\s*=\s*["\']([^"\']+)["\']\)'),                              "Vaadin"),
    ],

    "C#": [
        (re.compile(r'\[(?:HttpGet|HttpPost|HttpPut|HttpDelete|HttpPatch|Route)\s*\(\s*["\']([^"\']+)["\']\)'), "ASP.NET Core"),
        (re.compile(r'Map(?:Get|Post|Put|Delete|Patch)\(\s*["\']([^"\']+)["\']\)'),                           "ASP.NET Core Endpoints"),
        (re.compile(r'\[Route\(\s*["\']([^"\']+)["\']\)'),                                                  "ASP.NET Route"),
    ],

    "Python": [
        (re.compile(r'@(?:app|bp|api)\.route\(\s*["\']([^"\']+)["\']\)'), "Flask / FastAPI"),
        (re.compile(r'path\(\s*["\']([^"\']+)["\']\)'),              "Django / FastAPI"),
        (re.compile(r'url\(\s*r?["\']([^"\']+)["\']\)'),             "Django (old style)"),
    ],
    "JavaScript":[
      (re.compile(
            r'\b(?:app|router)\.(get|post|put|delete|patch|all)\s*\(\s*["\']([^"\']+)["\']'
        ), "Express"),

        # NestJS: @Controller('/foo'), @Get('/bar') и т.п.
        (re.compile(
            r'@(?:Controller|Get|Post|Put|Delete|Patch)\(\s*["\']([^"\']+)["\']\)'
        ), "NestJS"),  
    ],
    "TypeScript":[
      (re.compile(
            r'\b(?:app|router)\.(get|post|put|delete|patch|all)\s*\(\s*["\']([^"\']+)["\']'
        ), "Express"),

        # NestJS: @Controller('/foo'), @Get('/bar') и т.п.
        (re.compile(
            r'@(?:Controller|Get|Post|Put|Delete|Patch)\(\s*["\']([^"\']+)["\']\)'
        ), "NestJS"),  
    ],
    "JavaScript/TypeScript": [
        # Express: app.get('/foo', ...), router.post('/bar', ...)
        (re.compile(
            r'\b(?:app|router)\.(get|post|put|delete|patch|all)\s*\(\s*["\']([^"\']+)["\']'
        ), "Express"),

        # NestJS: @Controller('/foo'), @Get('/bar') и т.п.
        (re.compile(
            r'@(?:Controller|Get|Post|Put|Delete|Patch)\(\s*["\']([^"\']+)["\']\)'
        ), "NestJS"),
    ],

    "Ruby": [
        (re.compile(r'\b(?:get|post|put|delete|patch|match)\s+["\']([^"\']+)["\']'), "Rails"),
        (re.compile(r'resource\s+:\w+,\s*path:\s*["\']([^"\']+)["\']'),          "Rails Resources"),
    ],

    "PHP": [
        (re.compile(r'Route::(?:get|post|put|delete|patch|any)\(\s*["\']([^"\']+)["\']\)'), "Laravel"),
        (re.compile(r'@Route\(\s*["\']([^"\']+)["\']\)'),                              "Symfony"),
    ],

    "Go": [
        (re.compile(r'\.\s*(Handle|HandleFunc|Get|Post|Put|Delete)\(\s*["\']([^"\']+)["\']\)'), "net/http"),
        (re.compile(r'router\.(?:GET|POST|PUT|DELETE)\(\s*["\']([^"\']+)["\']\)'),             "Gorilla Mux"),
    ],
}
AJAX_PATTERN = re.compile(
    r"(?:XMLHttpRequest|fetch|\$\.ajax)\([^)]+['\"]([^'\"]+)['\"]\)"
    r"|\." 
    r"ajax\([^)]+['\"]([^'\"]+)['\"]\)"
)
AJAX_PATTERN_EXT = re.compile(
    r"fetch\([^)]+['\"]([^'\"]+)['\"]\)"
    r"|XMLHttpRequest\([^)]+['\"]([^'\"]+)['\"]\)"
    r"|jQuery\.ajax\([^)]+['\"]([^'\"]+)['\"]\)"
)
PASSWORD_PATTERN = re.compile(r"(password|secret|token|apikey|access_key|client_secret)\s*[:=]\s*['\"]?([a-zA-Z0-9_!@#$%^&*()]+)['\"]?")

DEPENDENCY_FILES = {
    "Java": ["pom.xml", "build.gradle"],
    "PHP": ["composer.json"],
    "Python": ["requirements.txt"],
    "Go": ["go.mod"],
    "JavaScript": ["package.json"],
    "Ruby": ["Gemfile"]
}

JS_TECH_DETECTION = {
    "React": {"packages": ["react", "react-dom"], "type": "frontend"},
    "Angular": {"packages": ["@angular/core"], "type": "frontend"},
    "Vue": {"packages": ["vue"], "type": "frontend"},
    "Express": {"packages": ["express"], "type": "backend"}, 
    "NestJS": {"packages": ["@nestjs/core"], "type": "backend"},
    "TypeORM": {"packages": ["typeorm"], "type": "database"}
}

    
LANG_EXTENSIONS = {
    "Java": [".java"],
    "PHP": [".php"],
    "Python": [".py"],
    "Go": [".go"],
    "JavaScript": [".js", ".jsx", ".mjs", ".cjs",".ejs"],
    "TypeScript": [".ts", ".tsx"],
    "HTML": [".html", ".htm"],
    "CSS": [".css", ".scss", ".sass", ".less"],
    "Ruby": [".rb"],
    "Shell": [".sh", ".bash"],
    "Kotlin": [".kt", ".kts"],
    "Swift": [".swift"],
    "C/C++": [".c", ".cpp", ".h", ".hpp"],
    "C#": [".cs"],
    "SQL": [".sql"],
    "XML": [".xml"],
    "YAML": [".yaml", ".yml"],
    "JSON": [".json"],
    "Markdown": [".md"],
    "Docker": ["Dockerfile", ".dockerignore"],
    "Config": [".conf", ".cfg", ".ini"],
}

CONFIG_FILES = [
    ".env", ".env.local", ".env.prod", ".env.dev", ".project", 
    "Jenkinsfile", "docker-compose.yml", "webpack.config.js",
    "tsconfig.json", "package.json", "package-lock.json",
    "build.gradle", "pom.xml", "composer.json", "go.mod",
    "Gemfile", "Gemfile.lock", "requirements.txt", "setup.py",
    "Makefile", "nginx.conf", "apache.conf", ".gitignore",
    ".eslintrc", ".prettierrc", "babel.config.js", "jest.config.js"
]
CONFIG_PATTERNS = {
    # Spring Boot
    "application.properties": {"spring.datasource": "Spring Boot", "quarkus.datasource": "Quarkus"},
    "application.yml": {"spring:": "Spring Boot", "quarkus:": "Quarkus"},
    # Laravel / Symfony
    "composer.json": { '"laravel/framework"': "Laravel", '"symfony/symfony"': "Symfony" },
    # Express используется вместо Express.js
    "package.json": { '"express"': "Express", '"next"': "Next.js", '"react"': "React" },
    # Python
    "requirements.txt": { "Django": "Django", "Flask": "Flask", "fastapi": "FastAPI" },
    # Общие
    ".env": { "DB_CONNECTION=mysql": "MySQL", "DB_CONNECTION=pgsql": "PostgreSQL", "CACHE_DRIVER=redis": "Redis" }
}
LOG_FILES = [
    "*.log", "logs/*.log", "*.error.log", "*.access.log",
    "sqlnet.log", "syslog.php", "nginx-error.log", "apache-error.log"
]

DEPENDENCY_PATTERNS = {
    "Java": [
        # каждый кортеж: (имя файла, строка для поиска, категория, отображаемое имя технологии)
        ("pom.xml",    "spring-boot",   "backend", "Spring Boot"),
        ("pom.xml",    "quarkus",       "backend", "Quarkus"),
        ("pom.xml",    "junit",         "testing", "JUnit"),
        ("build.gradle","spring-boot",  "backend", "Spring Boot"),
        ("build.gradle","quarkus",      "backend", "Quarkus"),
        ("build.gradle","junit",        "testing", "JUnit"),
    ],
    "Python": [
        ("requirements.txt", "django",   "backend", "Django"),
        ("requirements.txt", "flask",    "backend", "Flask"),
        ("requirements.txt", "fastapi",  "backend", "FastAPI"),
        ("setup.py",         "django",   "backend", "Django"),
        ("setup.py",         "flask",    "backend", "Flask"),
        ("setup.py",         "fastapi",  "backend", "FastAPI"),
    ],
    "Go": [
        ("go.mod", "github.com/gin-gonic/gin", "backend", "Gin"),
    ],
    "PHP": [
        # для JSON-файла будем разбирать require
        ("composer.json", {"laravel/framework":"Laravel", "symfony/symfony":"Symfony"}, "backend"),
    ],
}

TECHNOLOGIES_BY_LANG = {
    "Java": {
        "frameworks": ["Spring Boot", "Quarkus", "Micronaut", "Jakarta EE", "Play Framework", "Vert.x"],
        "databases": ["Hibernate", "JPA", "MyBatis", "JDBC", "JOOQ"],
        "build_tools": ["Maven", "Gradle", "Ant"],
        "test_frameworks": ["JUnit", "TestNG", "Mockito", "AssertJ"],
        "devops": ["Docker", "Kubernetes", "Jenkins"]
    },
    "C#": {
        "frameworks": [".NET Core", ".NET Framework", "ASP.NET MVC", "ASP.NET Web API", "Blazor", "Xamarin"],
        "databases": ["Entity Framework", "Dapper", "ADO.NET", "NHibernate"],
        "build_tools": ["MSBuild", "NuGet", "Cake"],
        "test_frameworks": ["NUnit", "xUnit", "MSTest", "Moq"],
        "devops": ["Azure DevOps", "Octopus Deploy"]
    },
    "Python": {
        "frameworks": ["Django", "Flask", "FastAPI", "Pyramid", "Bottle", "Tornado"],
        "databases": ["SQLAlchemy", "Django ORM", "Psycopg", "PyMySQL", "MongoEngine"],
        "build_tools": ["pip", "Poetry", "Pipenv", "Setuptools"],
        "test_frameworks": ["pytest", "unittest", "nose", "Robot Framework"],
        "devops": ["Fabric", "Ansible"]
    },
    "JavaScript": {
        "frameworks": ["Express", "Koa", "NestJS", "Meteor"],
        "frontend": ["React", "Angular", "Vue", "Svelte", "Ember"],
        "databases": ["Sequelize", "TypeORM", "Mongoose", "Prisma"],
        "build_tools": ["npm", "yarn", "webpack", "vite"],
        "test_frameworks": ["Jest", "Mocha", "Jasmine", "Cypress"],
        "devops": ["PM2", "Docker"]
    },
    "TypeScript": {
        "frameworks": ["NestJS", "Express", "LoopBack"],
        "frontend": ["Angular", "React", "Vue", "Svelte"],
        "databases": ["TypeORM", "Prisma", "MikroORM"],
        "build_tools": ["tsc", "webpack", "esbuild"],
        "test_frameworks": ["Jest", "Mocha", "Jasmine"],
        "devops": ["PM2", "Docker"]
    },
    "PHP": {
        "frameworks": ["Laravel", "Symfony", "CodeIgniter", "Yii", "Zend"],
        "databases": ["Eloquent ORM", "Doctrine", "PDO"],
        "build_tools": ["Composer", "Phar"],
        "test_frameworks": ["PHPUnit", "Codeception", "PHPSpec"],
        "devops": ["Deployer", "Capistrano"]
    },
    "Go": {
        "frameworks": ["Gin", "Echo", "Fiber", "Beego"],
        "databases": ["GORM", "SQLx", "Ent"],
        "build_tools": ["go build", "GoReleaser"],
        "test_frameworks": ["testing", "Testify", "GoConvey"],
        "devops": ["Docker", "Kubernetes"]
    },
    "Ruby": {
        "frameworks": ["Ruby on Rails", "Sinatra", "Hanami"],
        "databases": ["Active Record", "Sequel", "ROM"],
        "build_tools": ["Bundler", "Rake"],
        "test_frameworks": ["RSpec", "Minitest", "Cucumber"],
        "devops": ["Capistrano", "Mina"]
    },
    "Swift": {
        "frameworks": ["Vapor", "Perfect", "Kitura"],
        "databases": ["Fluent", "GRDB", "Realm"],
        "build_tools": ["Swift Package Manager", "CocoaPods"],
        "test_frameworks": ["XCTest", "Quick", "Nimble"],
        "devops": ["Fastlane", "Xcode Server"]
    },
    "Kotlin": {
        "frameworks": ["Ktor", "Spring Boot", "Micronaut", "Vert.x"],
        "databases": ["Exposed", "JPA", "Hibernate"],
        "build_tools": ["Gradle", "Maven"],
        "test_frameworks": ["JUnit", "Kotest", "MockK"],
        "devops": ["Docker", "Kubernetes"]
    },
    "Rust": {
        "frameworks": ["Actix", "Rocket", "Warp"],
        "databases": ["Diesel", "SQLx", "SeaORM"],
        "build_tools": ["Cargo", "Rustup"],
        "test_frameworks": ["cargo test", "Mockall"],
        "devops": ["Docker", "Kubernetes"]
    },
    "Scala": {
        "frameworks": ["Play", "Akka", "Lift"],
        "databases": ["Slick", "Quill", "Doobie"],
        "build_tools": ["sbt", "Maven"],
        "test_frameworks": ["ScalaTest", "Specs2", "ScalaCheck"],
        "devops": ["Docker", "Kubernetes"]
    }
}
TECHNOLOGY_DETECTORS = {
    # Java
    "Spring Boot": [
        {"type": "file", "path": "pom.xml", "content": "spring-boot-starter"},
        {"type": "file", "path": "build.gradle", "content": "org.springframework.boot"},
        {"type": "dir", "path": "src/main/resources/application.properties"},
        {"type": "dir", "path": "src/main/resources/application.yml"},
        {"type": "code", "pattern": r"@SpringBootApplication"}
    ],
    "Quarkus": [
        {"type": "file", "path": "pom.xml", "content": "quarkus"},
        {"type": "file", "path": "build.gradle", "content": "io.quarkus"},
        {"type": "dir", "path": "src/main/resources/application.properties", "content": "quarkus"},
        {"type": "code", "pattern": r"@QuarkusMain"}
    ],
    
    # PHP
    "Laravel": [
        {"type": "file", "path": "artisan"},
        {"type": "file", "path": "composer.json", "content": "laravel/framework"},
        {"type": "dir", "path": "app/Http/Controllers"},
        {"type": "dir", "path": "resources/views"},
        {"type": "code", "pattern": r"use Illuminate\\"}
    ],
    "Symfony": [
        {"type": "file", "path": "bin/console"},
        {"type": "file", "path": "composer.json", "content": "symfony/framework-bundle"},
        {"type": "dir", "path": "config/packages"},
        {"type": "dir", "path": "src/Controller"},
        {"type": "code", "pattern": r"use Symfony\\"}
    ],
    
    # Python
    "Django": [
        {"type": "file", "path": "manage.py"},
        {"type": "file", "path": "requirements.txt", "content": "Django"},
        {"type": "dir", "path": "urls.py"},
        {"type": "dir", "path": "settings.py"},
        {"type": "code", "pattern": r"from django\.|import django"}
    ],
    "Flask": [
        {"type": "file", "path": "requirements.txt", "content": "Flask"},
        {"type": "code", "pattern": r"from flask import|@app\.route"},
        {"type": "file", "path": "app.py", "content": "Flask(__name__)"}
    ],
    
    # JavaScript/TypeScript
    "Express.js": [
        {"type": "file", "path": "package.json", "content": "express"},
        {"type": "code", "pattern": r"require\(['\"]express['\"]|import express from"},
        {"type": "code", "pattern": r"app\.(get|post|put|delete)"}
    ],
    "React": [
        {"type": "file", "path": "package.json", "content": "react"},
        {"type": "dir", "path": "src/components"},
        {"type": "code", "pattern": r"import React|React\.Component"}
    ],
    
    # C#
    "ASP.NET Core": [
        {"type": "file", "path": "*.csproj", "content": "Microsoft.AspNetCore"},
        {"type": "dir", "path": "Controllers"},
        {"type": "code", "pattern": r"\[HttpGet\]|\[Route\("}
    ],
    
    # Ruby
    "Ruby on Rails": [
        {"type": "file", "path": "Gemfile", "content": "rails"},
        {"type": "file", "path": "config/routes.rb"},
        {"type": "dir", "path": "app/controllers"},
        {"type": "code", "pattern": r"class ApplicationController < ActionController::Base"}
    ],
    
    # Databases
    "MySQL": [
        {"type": "file", "path": ".env", "content": "DB_CONNECTION=mysql"},
        {"type": "code", "pattern": r"mysql://|mysql2?\.createConnection"}
    ],
    "PostgreSQL": [
        {"type": "file", "path": ".env", "content": "DB_CONNECTION=pgsql"},
        {"type": "code", "pattern": r"postgres://|pg\.connect"}
    ],
    
    # Build tools
    "Maven": [
        {"type": "file", "path": "pom.xml"}
    ],
    "Gradle": [
        {"type": "file", "path": "build.gradle"}
    ],
    
    # Testing frameworks
    "JUnit": [
        {"type": "file", "path": "pom.xml", "content": "junit"},
        {"type": "code", "pattern": r"@Test|import org\.junit"}
    ],
    "pytest": [
        {"type": "file", "path": "requirements.txt", "content": "pytest"},
        {"type": "code", "pattern": r"def test_|import pytest"}
    ],
    # TypeScript
    "NestJS": [
        {"type": "file", "path": "package.json", "content": "@nestjs/core"},
        {"type": "code", "pattern": r"@(Controller|Get|Post|Injectable)\("},
        {"type": "dir", "path": "src/controllers"}
    ],
    "Express": [
        {"type": "file", "path": "package.json", "content": "express"},
        {"type": "code", "pattern": r"app\.(get|post|put|delete)"},
        {"type": "code", "pattern": r"import express from ['\"]express['\"]"}
    ],
    "Angular": [
        {"type": "file", "path": "package.json", "content": "@angular/core"},
        {"type": "dir", "path": "src/app"},
        {"type": "code", "pattern": r"@Component\("}
    ],
    "React": [
        {"type": "file", "path": "package.json", "content": "react"},
        {"type": "dir", "path": "src/components"},
        {"type": "code", "pattern": r"import React|React\.Component"}
    ],
    "TypeORM": [
        {"type": "file", "path": "package.json", "content": "typeorm"},
        {"type": "code", "pattern": r"@Entity\("}
    ],
    # PHP frameworks
    "CodeIgniter": [
        {"type": "file", "path": "spark"},
        {"type": "dir", "path": "app/Controllers"},
        {"type": "code", "pattern": r"use CodeIgniter\\"},
        {"type": "file", "path": "composer.json", "content": "codeigniter4/framework"}
    ],
    
    "Composer": [
        {"type": "file", "path": "composer.json"},
        {"type": "file", "path": "composer.lock"},
        {"type": "dir", "path": "vendor"}
    ],
    
    "PHPUnit": [
        {"type": "file", "path": "phpunit.xml"},
        {"type": "file", "path": "composer.json", "content": "phpunit/phpunit"},
        {"type": "dir", "path": "tests"}
    ],
    "Next.js": [
        {"type": "file", "path": "package.json", "content": "next"},
        {"type": "dir", "path": "pages"},
        {"type": "code", "pattern": "import.*from ['\"]next['\"]"}
    ]
}