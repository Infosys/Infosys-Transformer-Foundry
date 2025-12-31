/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
import React from "react"
import { Link } from "react-router-dom"
export default function NavBar({ tab, children }: any) {
  const menu = ["tryout", "compare","promptlibrary"].map((menuName, index) => (
    <div key = {menuName} className="align-middle flex items-center"
     style={{padding: '0px 10px', alignItems: 'center', justifyContent: 'center', whiteSpace: 'nowrap', 
     ...(tab === menuName ? { borderBottom: '0.19rem solid #42619d' } : { borderBottom: '0.19rem solid #fffff' })}}>
      <Link
        to={`/${index > 0 ? menuName: ''}`}
        className={
          tab === menuName
            ? "cursor-default"
            : "cursor-pointer"
        }>
        <p
          className={
            tab === menuName
            ? "text-black-500"
            : "font-medium text-gray-500"
          }
          style={{ fontSize: '17px !important',
                   padding: '0px 24px', fontFamily: 'Roboto, Helvetica Neue, sans-serif', lineHeight: '1.5px', display: 'inline-flex', justifyContent: 'center', alignItems: 'center', whiteSpace: 'nowrap' }}
        >
          {/* {menuName.charAt(0).toUpperCase() + menuName.slice(1)} */}
          {String.fromCharCode(10112 + index) + " "}{menuName.charAt(0).toUpperCase() + menuName.slice(1)}
        </p>
      </Link>
    </div>
  ))

  return (
    <div className="flex flex-col font-display mb-3" style={{ height: '25px', backgroundColor: 'white'}}>
      <div className="flex inline-block mx-5 my-4 gap-x-4 flex-wrap" style={{margin: '0px 10px'}}>
        {menu}

        <div className ="flex-1" />

        {children}
      </div>
    </div>
  )
}