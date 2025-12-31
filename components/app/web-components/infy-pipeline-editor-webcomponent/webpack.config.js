
<!--
 ================================================================================================================
 # ===============================================================================================================
 # Copyright 2025 Infosys Ltd.
 # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at
 # http://www.apache.org/licenses/
 # ===============================================================================================================
 ================================================================================================================
-->
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: "./src/index.js",
  output: {
    path: "C:/Infosys-OpenSrc/transformer-studio-ui/src/assets",
    filename: "pipeline-editor-bundle.js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-react"],
          },
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./index.html",
    }),
  ],
  devServer: {
    static: {
      directory: path.join(__dirname, "dist"),
    },
    port: 3000,
  },
  devtool: "eval-source-map",
};
