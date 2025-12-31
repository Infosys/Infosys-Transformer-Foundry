/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
import { useCallback, useEffect, useLayoutEffect, useRef } from "react"

export const useCtrlMetaKeyPress = (keys: any, callback: any, node = null) => {
  const callbackRef = useRef(callback)
  useLayoutEffect(() => {
    callbackRef.current = callback
  })

  const handleKeyPress = useCallback(
    (event: any) => {
      if (event.metaKey && event.ctrlKey && keys.some((key: any) => event.key === key)) {
        callbackRef.current(event)
      }
    },
    [keys]
  )

  useEffect(() => {
    const targetNode = node ?? document
    targetNode && targetNode.addEventListener("keydown", handleKeyPress)

    return () =>
      targetNode && targetNode.removeEventListener("keydown", handleKeyPress)
  }, [handleKeyPress, node])
}