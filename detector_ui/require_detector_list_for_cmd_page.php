<div class="clearfix"></div>
<div id = "selected_detetors" class="row common_margin">

</div>
<div class="clearfix"></div>

<div class="row common_margin">
    <table id="maintable" class="table table-hover tbl_font_size "
           style="border: 1px solid lightgray;border-collapse: inherit">
        <thead class="thead">
        <tr >
            <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
            <!--<th width="2%"></th>-->
            <th width="10%">检测器编号</th>
            <th width="10%">生产厂商</th>
            <th width="10%">部署位置</th>
            <th width="10%">部署单位</th>
            <th width="10%">是否在线</th>
            <th width="10%">最后告警产生时间</th>
        </tr>
        </thead>

        <tbody>
        </tbody>

        <tfoot>
        <tr>
            <td><input type="checkbox" class="checkbox" id="chk_all2"></td>
            <td colspan="9">

                <div class="pull-right">

                    <?php
                    require_once(dirname(__FILE__) . '/require_page_bar_for_all_page.php');
                    ?>

<!--                    <nav id="paginationbox">
                        <span style="vertical-align:10px;">共有<strong id="totalcount2"></strong>条，每页显示：<strong>10</strong>条</span>
                        <ul id="pagination" class="pagination pagination-sm" style="margin: 0%;"> </ul>
                    </nav>-->
                </div>
            </td>
        </tr>

        </tfoot>
    </table>
</div>