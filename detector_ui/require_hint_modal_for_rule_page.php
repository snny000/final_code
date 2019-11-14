<div class="modal fade" id="hintModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    提示框
                </h4>
            </div>
            <div class="modal-body" style="text-align: center">
                <p style="color: red"></p>
                <p></p>
                <p></p>
                <p></p>
            </div>
            <div id="new_label_div" style="display: none;text-align: center;">
                <span>新备注标签1：</span> <input id="new_label" type="text" class="form-control" style="width: 250px !important;display: inline-block !important;">
                <div style="color:red"></div>
            </div>


            <!--       class="modal-footer"-->

            <div class="modal-footer">
                <button id="delSubmit" type="button" class="btn btn-primary">确定</button>

                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>

                <!--  <button id="cancelSubmit" type="button" class="btn btn-primary">关闭</button>-->


                <!-- data-dismiss="modal"-->
                <!-- <button id="cancelSubmit1" type="button" class="btn btn-default">关闭</button>-->


            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div class="modal fade" id="taskGroupModal" tabindex="-1" role="dialog" aria-labelledby="taskGroupLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    更新策略的任务组
                </h4>
            </div>
            <div class="modal-body" style="text-align: center">
                <div class="row">
                    <div class="operateTooltip"></div>
                    <label for="lunch">选择任务组:</label>
                    <select id="lunch" class="selectpicker task_group_select" data-live-search="true"  title="请选择任务组 ...">
                        <!--<option value="chinese">国庆</option>
                        <option value="hotdog">中秋</option>
                        <option>19大</option>
                        <option>house</option>
                        <option>home</option>-->
                    </select>
                </div>
            </div>

            <!--       class="modal-footer"-->

            <div class="modal-footer">
                <button id="taskGroupSubmit" type="button" class="btn btn-primary">确定</button>

                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>


            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<!-- 模态框（Modal） -->
<div class="modal fade" id="impModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    导入文件
                </h4>
            </div>
            <div class="modal-body">

                <div>
                    <p style="border:solid 1px #E3E3E3"><input type="file" id="upfile" ></p>
                    <p style="text-align:center">
                        <input type="button" id="upJQuery" value="上传文件" class="btn btn-primary" >
                    </p>
                    <div style='color:red;margin-top: 4px;text-align:center'></div>
                    <input id="param" hidden>
                </div>

            </div>

            <div class="modal-footer">
                <button id="imp-submit" type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<!--查看任务组-->
<!-- 模态框（Modal） -->
<div class="modal fade" id="showTaskGroupModal" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    任务组描述
                </h4>
            </div>
            <div class="modal-body">
                <div>
                    <span>任务组编号:</span> 
                    <input id="show_task_group_id" class="form-control" disabled>
                    <span>任务组名称:</span> 
                    <input id="show_task_group_name" class="form-control" disabled>
                    <span>策略种类:</span> 
                    <input id="show_task_group_type" class="form-control" disabled>
                    <span>创建者:</span> 
                    <input id="show_task_group_create" class="form-control" disabled>
                    <span>创建时间:</span> 
                    <input id="show_task_group_create_time" class="form-control" disabled>
                    <span>备注:</span> 
                    <input id="show_task_group_remark" class="form-control" disabled>
                    <div>
                </div>

            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-interval btn-primary" onclick="getTaskGroupRules()">查看相关策略</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>