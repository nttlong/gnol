angularDefine(function(mdl){
    mdl.service("$files",[function(){
        function FileLoader(ele,chunkSize){
            this._chunkSize=chunkSize||(1024*100);
            this._fileSize=0;
            this.ele=ele;
            var me=this;
            ele._owner=this;
            ele.onchange=me.readFile
            
        }
        FileLoader.prototype.onProgress=function(callback){
            this._onProgress=callback;
            return this;
        }
        FileLoader.prototype.onComplete=function(callback){
            this._onComplete=callback;
            return this;
        }
       
        FileLoader.prototype.readFile=function(evt){
            var me=evt.target._owner;
            var file=evt.target.files[0];
            me.fileName=file.name;
            var bPos = 0,
                mx = file.size,
                BUFF_SIZE = me._chunkSize,
                i = 0,
                collection = [],
                lineCount = 0;
            var d1 = +new Date;
            var remainder = "";
            var total=0;
            var chunkLen= Math.floor(file.size/me._chunkSize);
            if(file.size % me._chunkSize>0){
                chunkLen+=1;
            }

            function grabNextChunk() {
                
                var myBlob = file.slice(BUFF_SIZE * i, (BUFF_SIZE * i) + BUFF_SIZE, file.type);
                i++;
                var fr = new FileReader();
               
                fr.onload = function(e) {
                   
                    total+=me._chunkSize;
                    var remain = file.size-total;
                    if(remain<0){
                        remain=file.size - remain-me._chunkSize
                    }
                    var r= {
                        result: e.target.result,
                        index:i-1,
                        len:file.size,
                        strFileSize:me.getHumanFileSize(file.size),
                        strRemain:me.getHumanFileSize(remain),
                        strUploadedSize:me.getHumanFileSize((total<=file.size)?total:file.size),
                        chunkLen:chunkLen,
                        total:(total<=file.size)?total:file.size,
                        percent:(((total<=file.size)?total:file.size)/file.size)*100,
                        remain:remain,
                        originFileName:me.fileName
                    }
                    if(i<=chunkLen){
                        if(me._onProgress){
                       
                            me._onProgress(undefined,r,grabNextChunk)
                        }
                    }
                    else{
                        if(me._onComplete){
                            me._onComplete(me);
                        }
                    }
                    
                    

                };
                fr.readAsDataURL(myBlob, myBlob.type);
            } /* end grabNextChunk() */

            grabNextChunk();
        };
        FileLoader.prototype.getHumanFileSize=function(bytes, si) {
            var si=si||true;
            var thresh = si ? 1000 : 1024;
            if(Math.abs(bytes) < thresh) {
                return bytes + ' B';
            }
            var units = si
                ? ['kB','MB','GB','TB','PB','EB','ZB','YB']
                : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
            var u = -1;
            do {
                bytes /= thresh;
                ++u;
            } while(Math.abs(bytes) >= thresh && u < units.length - 1);
            return bytes.toFixed(1)+' '+units[u];
        }

        return function(ele){
             return new FileLoader(ele);
        }
    }]);
});