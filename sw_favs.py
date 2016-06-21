''' Plugin for Synwrite
Authors:
    Andrey Kvichansky    (kvichans on github.com)
    Alexey T (Synwrite)
Version:
    '1.0.2 2016-06-21'
ToDo: (see end of file)
'''

import  re, os, json
import	sw				as app 
from 	sw 			import ed
from    .sw_plug_lib    import *
from collections import OrderedDict as OrdDict

# I18N
_       = get_translation(__file__)

pass;                           # Logging
pass;                          #from pprint import pformat
pass;                          #pfrm15=lambda d:pformat(d,width=15)
pass;                           LOG = (-2==-2)  # Do or dont logging.

GAP     = 5

fav_json= app.app_ini_dir()+os.sep+'syn_favorites.json'

class Command:
    def add_filename(self, fn):
        if not fn:  return
        app.msg_status(_('Added to Favorites: ')+fn)
        
        stores  = json.loads(open(fav_json).read(), object_pairs_hook=OrdDict) \
                    if os.path.exists(fav_json) else OrdDict()
        files   = stores.get('fv_files', [])
        if any([os.path.samefile(fn, f) for f in files]):   return
        files  += [fn]
        stores['fv_files'] = files
        open(fav_json, 'w').write(json.dumps(stores, indent=4))
    
    def add_cur_file(self):
        self.add_filename(ed.get_filename())
        
    def add_cur_project(self):
        self.add_filename(app.file_get_name(app.FILENAME_PROJECT))
    def dlg(self):
        pass;                  #LOG and log('=',())
        stores  = json.loads(open(fav_json).read(), object_pairs_hook=OrdDict) \
                    if os.path.exists(fav_json) else OrdDict()
        files   = stores.get('fv_files', [])
        fold    = stores.get('fv_fold', True)
        last    = stores.get('fv_last', 0)
        while True:
            hasf= bool(files)
            itms= [f('{} ({})', os.path.basename(fv), os.path.dirname(fv)) for fv in files] \
                    if fold else \
                  [f('{}'     , os.path.basename(fv)                     ) for fv in files]
            itms= itms if itms else [' ']
            btn,vals,chds   = dlg_wrapper(_('Favorites'), GAP+500+GAP,GAP+300+GAP,     #NOTE: dlg-favorites
                 [dict(           tp='lb'   ,t=GAP          ,l=GAP          ,w=400      ,cap=_('&Files:')                       ) # &f
                 ,dict(cid='fvrs',tp='lbx'  ,t=GAP+20,h=250 ,l=GAP          ,w=400-GAP  ,items=itms                     ,en=hasf) # 
                 ,dict(cid='open',tp='bt'   ,t=GAP+20       ,l=GAP+400      ,w=100      ,cap=_('&Open')     ,props='1'  ,en=hasf) #     default
                 ,dict(cid='addc',tp='bt'   ,t=GAP+75       ,l=GAP+400      ,w=100      ,cap=_('&Add opened')                   ) # &a
                 ,dict(cid='brow',tp='bt'   ,t=GAP+100      ,l=GAP+400      ,w=100      ,cap=_('Add&...')                       ) # &.
                 ,dict(cid='delt',tp='bt'   ,t=GAP+135      ,l=GAP+400      ,w=100      ,cap=_('&Delete')               ,en=hasf) # &d
                 ,dict(cid='fvup',tp='bt'   ,t=GAP+210      ,l=GAP+400      ,w=100      ,cap=_('Move &up')              ,en=hasf) # &u
                 ,dict(cid='fvdn',tp='bt'   ,t=GAP+235      ,l=GAP+400      ,w=100      ,cap=_('Move do&wn')            ,en=hasf) # &w
                 ,dict(cid='fold',tp='ch'   ,tid='-'        ,l=GAP          ,w=100      ,cap=_('Show &paths')   ,act='1'        ) # &p
                 ,dict(cid='-'   ,tp='bt'   ,t=GAP+300-28   ,l=GAP+500-100  ,w=100      ,cap=_('Close')                         )
                 ],    dict(fvrs=last
                           ,fold=fold), focus_cid='fvrs')
            if btn is None or btn=='-': return None
            
#           store_b = fold != vals['fold']
            fold    = vals['fold']
            last    = vals['fvrs']
            if btn=='open' and files and last>=0 and os.path.isfile(files[last]):
                app.file_open(files[last])
                break#while
            
            # Modify
            store_b = 'fold' in chds
            if False:pass
            elif btn=='addc':
                fn      = ed.get_filename()
                if fn and not any([os.path.samefile(fn, f) for f in files]):
                    files  += [fn]
                    store_b = True
            elif btn=='brow':
                fn      = app.dlg_file(True, '', '', '')
                if fn and not any([os.path.samefile(fn, f) for f in files]):
                    files  += [fn]
                    store_b = True
            elif btn=='delt' and files and last>=0:
                del files[last]
                last    = max(0, len(files)-1)
                store_b = True
            elif btn in ('fvup', 'fvdn') and files:
                newp    = last + (-1 if btn=='fvup' else +1)
                if 0<=newp<len(files):
                    files[last], files[newp] = files[newp], files[last]
                    last    = newp
                    store_b = True
            
            # Store
            if store_b:
                stores['fv_files'] = files
                stores['fv_fold' ] = fold 
                stores['fv_last' ] = last 
                open(fav_json, 'w').write(json.dumps(stores, indent=4))
           #while
       #def dlg
   #class Command

'''
ToDo
[+][at-kv][20jun16] Moved from cuda_ext
'''
