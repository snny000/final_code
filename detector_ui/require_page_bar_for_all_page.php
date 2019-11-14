<nav id="paginationbox">
    <span style="vertical-align:10px;">共有<strong id="totalcount"></strong>条，每页显示：<!--<strong id="p_size">10</strong>-->
            <select id="p_size" onchange="selectPsize()" style="height:24px;border-radius:4px;">
                <option value='10'>10</option>
                <option value='20'>20</option>
                <option value='50'>50</option>
                <option value='100'>100</option>
            </select>
        条</span>
    <ul id="pagination" class="pagination pagination-sm" style="margin: 0%;"></ul>
    <input type="text" class="form-control"
           style="width: 50px;display: inline;height:29px; margin: 0%;vertical-align: 9px;border-radius: 4px;" id="pn"
           placeholder="">
    <input type="button" class="form-control btn btn-primary"
           style="width: 50px;display: inline;height:29px;margin: 0%;vertical-align: 8px;border-radius: 4px;padding: 5px 12px;"
           id="gotopn" value="跳转"">
</nav>