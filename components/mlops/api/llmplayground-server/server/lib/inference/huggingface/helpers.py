#  ================================================================================================================# 
# # ===============================================================================================================# 
# # Copyright 2024 Infosys Ltd.                                                                                    # 
# # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# # http://www.apache.org/licenses/                                                                                # 
#  ================================================================================================================# 
# from transformers import StoppingCriteria
import torch

class StoppingCriteriaSub(StoppingCriteria):
    def __init__(self, stops = []):
      StoppingCriteria.__init__(self), 

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, stops = []):
      self.stops = stops
      for i in range(len(stops)):
        self.stops = self.stops[i]