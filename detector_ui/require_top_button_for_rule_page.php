<button id="addButton" type="button" class="btn btn-interval btn-primary" data-toggle="modal" data-target="#addModal"><i class="fa fa-plus">&nbsp;&nbsp;</i>添加</button>
<!--<button id="x3" type="button" class="btn btn-primary btn-interval" ><i class="fa fa-file">&nbsp;&nbsp;</i>导入文件</button>-->
<button class="btn btn-interval btn-primary" id="export" onclick="export_file()">导入模板下载</button>
<button id="x3" type="button" class="btn btn-primary btn-interval"  data-toggle="modal" data-target="#impModal"><i class="fa fa-file">&nbsp;&nbsp;</i>导入文件</button>
<div class="btn-group btn-interval">
                    <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown"><i class="fa fa-hourglass">&nbsp;&nbsp;</i>同步
                        <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu" role="menu">                       
                        <li><a id="full" href="#">刷新检测器策略集<span hidden="">16</span></a></li>
                        <li class="divider"></li>
                        <li><a id="fullCenter" href="#">上报管理中心策略集</a></li>
                    </ul>
                </div>
<!-- <button id="full" type="button" class="btn btn-primary btn-interval" ><i class="fa fa-hourglass">&nbsp;&nbsp;</i>全量&nbsp;<span hidden></span></button> -->
<button id="increment" type="button" class="btn btn-primary btn-interval" ><i class="fa fa-hourglass-half">&nbsp;&nbsp;</i>增量&nbsp;<span class="badge" style="background-color:orange"></span></button>
