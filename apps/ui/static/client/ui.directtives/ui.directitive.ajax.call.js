angularDefine(function(mdl){
    /**
 * <call [component-id="{name}"] data-id="ajax function name" [data-params="param variable"] [data-callback="callback function name"] [data-function="function name"/>
 */
mdl.directive("call",["$parse",function($parse){
    return {
        restrict:"ECA",
        priority:2,
        scope:false,
        link:function(s,e,a){
            $(e[0]).hide();
            s.$watch(e.parent().attr("ws")||"$ws",function(o,v){
                var scope=findScopeById($(e.parents("[scope-id]")[0]).attr("scope-id")*1)||s;
                var ws=undefined;
                function exec(params,callback,noMask){
                        var data=params||scope.$eval(a.params);
                        ws.call(a.id,data,function(e,r){
                            if(e){
                                throw(e);
                                return;
                            }
                            if(callback){
                                callback(r);
                                return;
                            }
                            if(a.callback){
                                var fn=scope.$eval(a.callback);
                                if(angular.isFunction(fn)){
                                    fn(r);
                                }
                            }
                            if(a.ngModel){
                                $parse(a.ngModel).assign(scope,r);
                                scope.$applyAsync();
                            }
                        },noMask||a.noMask);
                }
                if(angular.isDefined(v)){
                    ws=v;
                    
                    if(a.componentId){
                        function ajaxComponent(exec){
                            this._exec=exec
                            this.ajaxComponent=true;
                        }
                        ajaxComponent.prototype.noMask=function(){
                            this._noMask=true;
                            return this;
                        }
                        ajaxComponent.prototype.before=function(callback){
                            this._before=callback;
                            return this;
                        }
                        ajaxComponent.prototype.after=function(callback){
                            this._after=callback;
                            return this;
                        }
                        ajaxComponent.prototype.params=function(pars){
                            this._params=pars;
                            this._id = a.id;
                            return this;
                        };
                        ajaxComponent.prototype.done=function(callback){
                            var me=this;
                            if(this._before){
                                var fn=scope.$eval(this._before);
                                if(angular.isFunction(fn)){
                                    fn(this);
                                }
                                
                            }
                            this._exec(this._params,function(res){
                                if(me._after){
                                    var fn=scope.$eval(me._after);
                                    if(angular.isFunction(fn)){
                                        fn(me);
                                    }
                                }
                                var fn2=scope.$eval(callback);
                                if(angular.isFunction(fn2)){
                                    fn2(me);
                                }
                                
                            });
                            return;
                        }
                        
                        

                        var cmp=    new ajaxComponent(exec);
                        console.log(cmp);
                        $parse(a.componentId).assign(scope,cmp);
                        return;
                    }
                    if(a.id && (!a.function)&&(!a.componentId)){
                        exec();

                    }
                    else {
                        $parse(a.function).assign(scope,exec);
                    }
                }
            })
            
        }
    }
}])


})