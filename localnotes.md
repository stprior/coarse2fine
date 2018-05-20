(coarse2fine) [stevop@gyfu coarse2fine]$ conda install pytorch cuda91 -c pytorch
Fetching package metadata .............
Solving package specifications: .

Package plan for installation in environment /home/stevop/.conda/envs/coarse2fine:

The following NEW packages will be INSTALLED:

    cffi:           1.11.5-py35h9745a5d_0                     
    cuda91:         1.0-h4c16780_0                     pytorch
    intel-openmp:   2018.0.0-8                                
    libgfortran-ng: 7.2.0-hdf63c60_3                          
    mkl:            2018.0.2-1                                
    mkl_fft:        1.0.1-py35h3010b51_0                      
    mkl_random:     1.0.1-py35h629b387_0                      
    ninja:          1.8.2-py35h6bb024c_1                      
    numpy:          1.14.2-py35hdbf6ddf_1                     
    pycparser:      2.18-py35h61b3040_1                       
    pytorch:        0.4.0-py35_cuda9.1.85_cudnn7.1.2_1 pytorch [cuda91]

---

removed torch from requirements.txt
ran pip install -r requirements.txt

Successfully built nltk tabulate forked-path tablib docopt SQLAlchemy odfpy openpyxl unicodecsv pyyaml et-xmlfile
mkl-random 1.0.1 requires cython, which is not installed.
mkl-fft 1.0.0 requires cython, which is not installed.

coarse2fine) [stevop@gyfu coarse2fine]$ conda install cython
Fetching package metadata ...........
Solving package specifications: .

Package plan for installation in environment /home/stevop/.conda/envs/coarse2fine:

The following NEW packages will be INSTALLED:

    cython: 0.28.2-py35h14c3975_0

---

(coarse2fine) [stevop@gyfu coarse2fine]$ ./pretrain.sh wikisql 0
Traceback (most recent call last):
  File "evaluate.py", line 9, in <module>
    import table
  File "/home/stevop/repos/coarse2fine/wikisql/table/__init__.py", line 2, in <module>
    import table.Models
  File "/home/stevop/repos/coarse2fine/wikisql/table/Models.py", line 9, in <module>
    from table.Utils import aeq, sort_for_pack
  File "/home/stevop/repos/coarse2fine/wikisql/table/Utils.py", line 2, in <module>
    from path import Path
  File "/home/stevop/.conda/envs/coarse2fine/lib/python3.5/site-packages/path.py", line 946
    def mkdir(self, mode=0777):

This is due to forked_path in requirements.txt - which is not compatible with python3.5
cloned latest forked_path from git and overwrote path.py

---

coarse2fine) [stevop@gyfu coarse2fine]$ ./pretrain.sh wikisql 0
Traceback (most recent call last):
  File "evaluate.py", line 9, in <module>
    import table
  File "/home/stevop/repos/coarse2fine/wikisql/table/__init__.py", line 2, in <module>
    import table.Models
  File "/home/stevop/repos/coarse2fine/wikisql/table/Models.py", line 9, in <module>
    from table.Utils import aeq, sort_for_pack
  File "/home/stevop/repos/coarse2fine/wikisql/table/Utils.py", line 2, in <module>
    from path import Path
ImportError: cannot import name 'Path'

changed Utils.py to import path

---

Error looking for WikiSQL files;
(coarse2fine) [stevop@gyfu coarse2fine]$ ./pretrain.sh wikisql 0
Traceback (most recent call last):
  File "evaluate.py", line 9, in <module>
    import table
  File "/home/stevop/repos/coarse2fine/wikisql/table/__init__.py", line 4, in <module>
    import table.ParseResult
  File "/home/stevop/repos/coarse2fine/wikisql/table/ParseResult.py", line 3, in <module>
    from lib.dbengine import DBEngine
ImportError: No module named 'lib'

cloned WikiSQL and included it in PYTHONPATH

---

coarse2fine) [stevop@gyfu coarse2fine]$ ./pretrain.sh wikisql 0
Traceback (most recent call last):
  File "evaluate.py", line 9, in <module>
    import table
  File "/home/stevop/repos/coarse2fine/wikisql/table/__init__.py", line 6, in <module>
    from table.Translator import Translator
  File "/home/stevop/repos/coarse2fine/wikisql/table/Translator.py", line 6, in <module>
    import table.ModelConstructor
  File "/home/stevop/repos/coarse2fine/wikisql/table/ModelConstructor.py", line 13, in <module>
    from lib.query import agg_ops, cond_ops
ImportError: cannot import name 'agg_ops'

changed from lib.query import agg_ops, cond_ops to from lib.query import Query
changed agg_ops to Query.agg_ops
couldn't find cond_ops used
---

Traceback (most recent call last):
  File "evaluate.py", line 17, in <module>
    from path import Path
ImportError: cannot import name 'Path'

changed evaluate.py as before

---

Traceback (most recent call last):
  File "evaluate.py", line 85, in <module>
    main()
  File "evaluate.py", line 63, in main
    r_list += translator.translate(batch)
  File "/home/stevop/repos/coarse2fine/wikisql/table/Translator.py", line 96, in translate
    emb_op_t, q_all, cond_state)
  File "/home/stevop/.conda/envs/coarse2fine/lib/python3.5/site-packages/torch/nn/modules/module.py", line 491, in __call__
    result = self.forward(*input, **kwargs)
  File "/home/stevop/repos/coarse2fine/wikisql/table/Models.py", line 239, in forward
    outputs = torch.stack(outputs)
TypeError: stack(): argument 'tensors' (position 1) must be tuple of Tensors, not Tensor

changed Models.py to torch.stack([outputs])
Same with torch.stack(attns[k])

---

Traceback (most recent call last):
  File "evaluate.py", line 85, in <module>
    main()
  File "evaluate.py", line 63, in main
    r_list += translator.translate(batch)
  File "/home/stevop/repos/coarse2fine/wikisql/table/Translator.py", line 99, in translate
    cond_context, tbl_enc, tbl_mask).data)
  File "/home/stevop/.conda/envs/coarse2fine/lib/python3.5/site-packages/torch/nn/modules/module.py", line 491, in __call__
    result = self.forward(*input, **kwargs)
  File "/home/stevop/repos/coarse2fine/wikisql/table/Models.py", line 182, in forward
    r_list.append(self.sel_match(cond_context_one, tbl_enc, tbl_mask))
  File "/home/stevop/.conda/envs/coarse2fine/lib/python3.5/site-packages/torch/nn/modules/module.py", line 491, in __call__
    result = self.forward(*input, **kwargs)
  File "/home/stevop/repos/coarse2fine/wikisql/table/Models.py", line 151, in forward
    tbl_enc.size(0), tbl_enc.size(1), q_enc.size(1))
RuntimeError: expand(torch.cuda.FloatTensor{[1, 1, 30, 250]}, size=[15, 30, 30]): the number of sizes provided (3) must be greater or equal to the number of dimensions in the tensor (4)

---

This is called from Translator.translate
cond_col = argmax(self.model.cond_col_match(
                cond_context, tbl_enc, tbl_mask).data)
Identify the condition column based on condition context, table encode and table mask
cond_col_match is defined in ModelConstructor as cond_col_match = CondMatchScorer(
        MatchScorer(2 * model_opt.rnn_size, model_opt.score_size, model_opt.dropout))


set up a new conda env and branch to try again with pytorch 0.2.0

--

coarse2finetorch2) [stevop@gyfu coarse2fine]$ ./pretrain.sh wikisql 0
/home/stevop/repos/coarse2fine/data_model/wikisql/pretrain.pt
/home/stevop/repos/coarse2fine/data_model/wikisql/annotated_ent/test.jsonl
Loading model
Traceback (most recent call last):
  File "evaluate.py", line 85, in <module>
    main()
  File "evaluate.py", line 63, in main
    r_list += translator.translate(batch)
  File "/home/stevop/repos/coarse2fine/wikisql/table/Translator.py", line 99, in translate
    cond_context, tbl_enc, tbl_mask).data)
  File "/home/stevop/.conda/envs/coarse2finetorch2/lib/python3.5/site-packages/torch/nn/modules/module.py", line 224, in __call__
    result = self.forward(*input, **kwargs)
  File "/home/stevop/repos/coarse2fine/wikisql/table/Models.py", line 182, in forward
    r_list.append(self.sel_match(cond_context_one, tbl_enc, tbl_mask))
  File "/home/stevop/.conda/envs/coarse2finetorch2/lib/python3.5/site-packages/torch/nn/modules/module.py", line 224, in __call__
    result = self.forward(*input, **kwargs)
  File "/home/stevop/repos/coarse2fine/wikisql/table/Models.py", line 151, in forward
    tbl_enc.size(0), tbl_enc.size(1), q_enc.size(1))
  File "/home/stevop/.conda/envs/coarse2finetorch2/lib/python3.5/site-packages/torch/autograd/variable.py", line 722, in expand
    return Expand.apply(self, sizes)
  File "/home/stevop/.conda/envs/coarse2finetorch2/lib/python3.5/site-packages/torch/autograd/_functions/tensor.py", line 111, in forward
    result = i.expand(*new_size)
RuntimeError: invalid argument 1: the number of sizes provided must be greater or equal to the number of dimensions in the tensor at /opt/conda/conda-bld/pytorch_1511318728473/work/torch/lib/THC/generic/THCTensor.c:309

Revert changes to wikisql/table/Models.py

---
*It worked!*

Loading model
Results:
all: 11412 / 15878 = 71.87%
exe: 12493 / 15878 = 78.68%

