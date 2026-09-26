package com.barad.runner;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.MimeTypeMap;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.InputStream;

public class MainActivity extends Activity {
    private WebView webView;
    private static final String ASSET_HOST = "appassets.androidplatform.net";

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        webView = new WebView(this);
        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        webView.setBackgroundColor(0xFF79C8EC);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        webView.setWebViewClient(new LocalAssetWebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        setContentView(webView);
        webView.loadUrl("https://appassets.androidplatform.net/assets/index.html");
    }

    private class LocalAssetWebViewClient extends WebViewClient {
        @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            return serveAsset(request.getUrl());
        }

        @SuppressWarnings("deprecation")
        @Override public WebResourceResponse shouldInterceptRequest(WebView view, String url) {
            return serveAsset(Uri.parse(url));
        }

        private WebResourceResponse serveAsset(Uri uri) {
            if (uri == null || !ASSET_HOST.equals(uri.getHost())) return null;
            String path = uri.getPath();
            if (path == null || !path.startsWith("/assets/")) return null;
            String assetPath = path.substring("/assets/".length());
            if (assetPath.isEmpty() || assetPath.contains("..")) return null;
            try {
                InputStream input = getAssets().open(assetPath);
                String ext = "";
                int dot = assetPath.lastIndexOf('.');
                if (dot >= 0 && dot < assetPath.length()-1) ext = assetPath.substring(dot+1).toLowerCase();
                String mime = MimeTypeMap.getSingleton().getMimeTypeFromExtension(ext);
                if (mime == null) {
                    if ("js".equals(ext) || "mjs".equals(ext)) mime = "text/javascript";
                    else if ("html".equals(ext)) mime = "text/html";
                    else mime = "application/octet-stream";
                }
                return new WebResourceResponse(mime, "UTF-8", 200, "OK", null, input);
            } catch (Exception ignored) {
                return null;
            }
        }
    }

    @Override protected void onDestroy() {
        if (webView != null) {
            webView.loadUrl("about:blank");
            webView.stopLoading();
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
}
