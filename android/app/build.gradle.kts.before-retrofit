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
    buildTypes {
        debug {
            val api = providers.gradleProperty("STUDYFLOW_API_URL").orElse("http://10.0.2.2:8000/api/").get()
            buildConfigField("String", "API_BASE_URL", "\"${api.replace("\\", "\\\\").replace("\"", "\\\"")}\"")
        }
        release {
            val api = providers.gradleProperty("STUDYFLOW_RELEASE_API_URL").orElse("").get()
            buildConfigField("String", "API_BASE_URL", "\"${api.replace("\\", "\\\\").replace("\"", "\\\"")}\"")
            optimization {
                enable = true
                packageScope = setOf("androidx.**", "kotlin.**", "kotlinx.**")
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
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