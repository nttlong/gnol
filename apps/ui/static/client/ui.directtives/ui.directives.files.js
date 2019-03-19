/*
    <b-file-upload data-on-sync data-on-error/>
*/

angularDefine(function(mdl){
    /*
        <fieldset>
            <legend>
                Select file to upload
            </legend>
            <input type="file" id="file"/>
            <ul>
                <li>
                    <span id="fileSize"></span>
                </li>
                <li>
                    <div id="myProgress">
                        <div id="myBar"></div>
                    </div>
                </li>
            </ul>
        </fieldset>
    */
      mdl.directive("bFileUpload",["$parse","$files",function($parse,$files){
          return {
              restrict:"CEA",
              replace:true,
              template:'<fieldset>'+
                        '<legend>'+
                        'Select file to upload'+
                        '</legend>'+
                        '<input type="file" id="file"/>'+
                        '<ul>'+
                        '<li>'+
                        '<span id="fileSize"></span>'+
                        '</li>'+
                        '<li>'+
                        '<div id="myProgress">'+
                        '<div id="myBar"></div>'+
                        '</div>'+
                        '</li>'+
                        '</ul>'+
                        '</fieldset>',
              link:function(s,e,a){
                   e.find("#myProgress").css({
                        width: "100%",
                        "background-color": "#ddd",
                        "float":"left"
                   });
                    var file = $files(e.find("#file")[0]);
                    file.onProgress(function(error,r,n){
                        if(!error){
                            if(a.onSync){
                                $parse(a.ngModel).assign(s,r);
                                var fn=s.$eval(a.onSync);
                                fn._exec(undefined,function(res){
                                    e.find("#fileSize").html("Uploaded size :{0}".replace("{0}",r.strUploadedSize+"/"+ r.strFileSize))
                                    e.find("#myBar").css({
                                        "width": r.percent+"%",
                                        "height": "30px",
                                        "background-color": "#4CAF50"
                                    });
                                    // e.find("#info").html(r.percent)
                                    n();
                                });
                            }
                        }
                    });
              }
          }
      }])      
});