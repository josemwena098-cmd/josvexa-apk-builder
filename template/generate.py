import os, re, json, html
i = re.sub(r'[^a-z0-9]', '', os.environ['APP_ID'].lower()) or 'app'
pkg = 'com.josvexa.w' + i
url = os.environ['APP_URL']; name = os.environ['APP_NAME']
def w(p, c):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True); open(p, 'w').write(c)
w('apk/settings.gradle', 'pluginManagement{repositories{google();mavenCentral();gradlePluginPortal()}}\ndependencyResolutionManagement{repositories{google();mavenCentral()}}\nrootProject.name="app"\ninclude ":app"\n')
w('apk/build.gradle', 'plugins{id "com.android.application" version "8.5.2" apply false}\n')
w('apk/gradle.properties', 'android.useAndroidX=true\norg.gradle.jvmargs=-Xmx2g\n')
w('apk/app/build.gradle', '''plugins{id "com.android.application"}
android{
 namespace "%s"
 compileSdk 34
 defaultConfig{applicationId "%s"
  minSdk 21
  targetSdk 34
  versionCode 1
  versionName "1.0"}
 signingConfigs{release{
  storeFile file(System.getenv("KS_FILE"))
  storePassword System.getenv("KS_PASS")
  keyAlias "josvexa"
  keyPassword System.getenv("KS_PASS")
  storeType "pkcs12"
  enableV1Signing true
  enableV2Signing true
  enableV3Signing true}}
 buildTypes{release{signingConfig signingConfigs.release
  minifyEnabled false}}
 compileOptions{sourceCompatibility JavaVersion.VERSION_1_8
  targetCompatibility JavaVersion.VERSION_1_8}
 lint{checkReleaseBuilds false
  abortOnError false}
 dependenciesInfo{includeInApk false
  includeInBundle false}
}
''' % (pkg, pkg))
w('apk/app/src/main/AndroidManifest.xml', '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28"/>
<uses-feature android:name="android.hardware.camera" android:required="false"/>
<uses-feature android:name="android.hardware.location" android:required="false"/>
<uses-feature android:name="android.hardware.microphone" android:required="false"/>
<application android:label="@string/app_name" android:icon="@mipmap/ic_launcher" android:roundIcon="@mipmap/ic_launcher" android:allowBackup="true" android:hardwareAccelerated="true" android:usesCleartextTraffic="true" android:theme="@android:style/Theme.Material.Light.NoActionBar">
<activity android:name=".MainActivity" android:exported="true" android:launchMode="singleTask" android:configChanges="orientation|screenSize|screenLayout|keyboardHidden|keyboard|smallestScreenSize|uiMode" android:windowSoftInputMode="adjustResize">
<intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter>
</activity>
</application>
</manifest>
''')
w('apk/app/src/main/res/values/strings.xml', '<resources><string name="app_name">%s</string></resources>\n' % html.escape(name).replace("'", "\\'").replace('@', '\\@').replace('?', '\\?'))
src = open('template/MainActivity.java').read().replace('__PKG__', pkg).replace('__URL__', json.dumps(url))
w('apk/app/src/main/java/%s/MainActivity.java' % pkg.replace('.', '/'), src)
