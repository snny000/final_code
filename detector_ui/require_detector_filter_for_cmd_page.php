<!--<div class="container-whole">-->
    <div id="searchDiv" class="row btn-banner" style="padding-left: 30px;">
        <div class="dropdown dropdown-inline">
            <button type="button" data-toggle="dropdown"
                    class="btn dropdown-btn dropdown-menu-width"
                    aria-haspopup="true"
                    aria-expanded="false">
                <span id="contractor" class="pull-left" value="00">所有厂商</span>
                <i class="fa fa-sort-down pull-right"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                <?php
                require_once(dirname(__FILE__) . '/require_contractor_list_for_all_page.php');
                ?>
            </ul>
        </div>

        <div class="dropdown btn-interval dropdown-inline">
            <button type="button" data-toggle="dropdown"
                    class="btn dropdown-btn dropdown-menu-width"
                    aria-haspopup="true"
                    aria-expanded="false">
                <span id="address_code" class="pull-left" value="0">所有位置</span>
                <i class="fa fa-sort-down pull-right"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                <li onclick="selectProtoFwd(this);" value="0">所有位置</li>
                <li onclick="selectProtoFwd(this);" value="100000">北京</li>
                <li onclick="selectProtoFwd(this);" value="200000">上海</li>
                <li onclick="selectProtoFwd(this);" value="510000">广州</li>
            </ul>
        </div>

        <div class="dropdown btn-interval dropdown-inline">
            <button type="button" data-toggle="dropdown"
                    class="btn dropdown-btn dropdown-menu-width"
                    aria-haspopup="true"
                    aria-expanded="false">
                <span id="device_status" class="pull-left" value="1">正常运行</span>
                <i class="fa fa-sort-down pull-right"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                <li onclick="selectProtoFwd(this);" value="1">正常运行</li>
                <li onclick="selectProtoFwd(this);" value="0">所有状态</li>
                <li onclick="selectProtoFwd(this);" value="2">暂未审核</li>
                <li onclick="selectProtoFwd(this);" value="3">审核失败</li>
                <li onclick="selectProtoFwd(this);" value="4">认证失败</li>
                <li onclick="selectProtoFwd(this);" value="5">流量异常</li>
                <li onclick="selectProtoFwd(this);" value="6">系统异常</li>
                <li onclick="selectProtoFwd(this);" value="7">资源异常</li>
                <li onclick="selectProtoFwd(this);" value="8">策略异常</li>
            </ul>
        </div>

        <input id="device_id" type="text" class="form-control search-input btn-interval" placeholder="检测器ID(模糊搜索)">
        <input id="user" type="text" class="form-control search-input btn-interval" placeholder="部署单位(模糊搜索)">
        <button id="searchButton" type="button" class="btn btn-primary btn-interval"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
        <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>


        <!-- value用于标记是否已经点击查询的逻辑 -->
        数量：<span id="totalcount" value="0" style="color: red;font-size: large;font-weight: bold">？</span>

    </div>
<!--</div>-->