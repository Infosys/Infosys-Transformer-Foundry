/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

//Needed for MFE Application
const concat = require("concat");
(async function build() {
  const files = [
    "./dist/mfe-tf-leaderboard/runtime.js",
    "./dist/mfe-tf-leaderboard/polyfills.js",
    "./dist/mfe-tf-leaderboard/main.js",
  ];
  await concat(files, "./dist/mfe-tf-leaderboard/mfe-tf-leaderboard.js");
})();