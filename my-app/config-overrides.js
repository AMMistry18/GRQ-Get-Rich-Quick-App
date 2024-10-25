const path = require('path');

module.exports = function override(config, env) {
  // Add fallbacks for Node.js core modules
  config.resolve.fallback = {
    fs: false, // No polyfill for fs, since it's not needed in the browser
    path: require.resolve("path-browserify"),
    url: require.resolve("url"),
    process: require.resolve("process/browser"),
  };

  return config;
};