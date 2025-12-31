/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Pipe, PipeTransform } from "@angular/core";
import { DatePipe } from "@angular/common";

@Pipe({
  name: "dateFormat",
})
export class DateFormatPipe implements PipeTransform {
  // This pipe is used to format the date in the format yyyy/MM/dd, hh:mm:ss a
  transform(value: string): string {
    const timestamp = parseInt(value);
    const datePipe = new DatePipe("en-US");
    const formattedDate = datePipe.transform(
      timestamp * 1000,
      "yyyy/MM/dd, hh:mm:ss a"
    );
    return formattedDate || "";
  }
}
