/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Pipe, PipeTransform } from '@angular/core';
import { format } from 'date-fns';

@Pipe({
  name: 'utcToLocal'
})
export class UtcToLocalPipe implements PipeTransform {

  // function to convert UTC date to local date
  transform(utcString: string): string {
    const utcDate = new Date(utcString);
    const localDate = new Date(utcDate.getTime() - utcDate.getTimezoneOffset() * 60 * 1000)
    const localDateFormatted = format(localDate, 'dd-MMM-yyyy');
    return localDateFormatted;
  }

}
