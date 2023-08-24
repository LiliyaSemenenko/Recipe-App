module.exports = {
    apps : [{
      name: "app",
      script: "./src/App.js",
      "watch": true,
      "autorestart": true,
      "ignore_watch": ["node_modules"],
      env: {
        NODE_ENV: "development",
      },
      env_production: {
        NODE_ENV: "production",
      }
    }]
}