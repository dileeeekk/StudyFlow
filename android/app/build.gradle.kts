plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.example.studyflowapp"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "com.example.studyflowapp"
        minSdk = 24
        targetSdk = 37
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildFeatures { buildConfig = true }

    signingConfigs {
        create("release") {
            storeFile = file("${System.getProperty("user.home")}/.android/studyflow-release.jks")
            storePassword = System.getenv("STUDYFLOW_KEYSTORE_PASSWORD")
                ?: ""
            keyAlias = "studyflow"
            keyPassword = System.getenv("STUDYFLOW_KEYSTORE_PASSWORD")
                ?: ""
        }
    }

    buildTypes {
        debug {
            val api = providers.gradleProperty("STUDYFLOW_API_URL").orElse("http://10.0.2.2:8000/api/").get()
            buildConfigField("String", "API_BASE_URL", "\"${api.replace("\\", "\\\\").replace("\"", "\\\"")}\"")
        }
        release {
            signingConfig = signingConfigs.getByName("release")
            val api = providers.gradleProperty("STUDYFLOW_RELEASE_API_URL").orElse("").get()
            buildConfigField("String", "API_BASE_URL", "\"${api.replace("\\", "\\\\").replace("\"", "\\\"")}\"")
            optimization {
                enable = false
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation("androidx.work:work-runtime:2.12.0")
    implementation("com.squareup.retrofit2:retrofit:3.0.0")
    implementation("com.squareup.retrofit2:converter-gson:3.0.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")

    implementation("androidx.lifecycle:lifecycle-viewmodel:2.11.0")
    implementation("androidx.lifecycle:lifecycle-livedata-core:2.11.0")
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.constraintlayout)
    implementation(libs.androidx.core.ktx)
    implementation(libs.material)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)
}
