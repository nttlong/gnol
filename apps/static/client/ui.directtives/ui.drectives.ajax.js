angularDefine(function(mdl){
    mdl.directive("ajax",["$ajax","$parse",function($ajax,$parse){
        return {
            restrict:"ECA",
            transclude:true,
            replace:true,
            priority:1,
            scope:false,
            template:"<ajax-caller ng-transclude></ajax-caller>",
            link:function(s,e,a){
                var scopeEles= $(e[0]).parents("[scope-id]");
                if(scopeEles.length==0){
                    e.attr("scope-id",angular.element(e[0]).scope().$id);
                }
                if(a.ws){
                    $parse(a.ws).assign(s,$ajax.with(a.url));
                }
                else {
                    $parse("$ws").assign(s,$ajax.with(a.url));
                }
            }
        }
    }]);
})