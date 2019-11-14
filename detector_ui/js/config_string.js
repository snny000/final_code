/**
 * Created by Fernando on 2016/7/7.
 */


function getTotal() {
    return 10;
}
function getTotalRulesNum() {
    return 30;
}
function getTotalAclNum() {
    return 10;
}


function getUploadCertificateModal(modal_id, tag) {
    var prefix = getPrefix(tag);
    var str = "<div class='modal fade' id='uploadCertificateModal" + prefix + modal_id + "'tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "                                                <div class='modal-dialog' role='document'>\n" +
        "                                                    <div class='modal-content'>\n" +
        "                                                        <div class=\"modal-header\">\n" +
        "                                                            <button type=\"button\" class=\"close\" onclick='closeDDosModals(this, 2);'\n" +
        "                                                                    aria-label=\"Close\"><span\n" +
        "                                                                    aria-hidden=\"true\">&times;</span></button>\n" +
        "                                                            <h4 class=\"modal-title\" id=\"myModalLabel1\">上传证书</h4>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-body'>\n" +
        "                                                            <div class='row certificate-row'>\n" +
        "                                                                <div class='col-md-3 certificate-name'><p>*证书内容</p>\n" +
        "                                                                </div>\n" +
        "                                                                <div class='col-md-8'>\n" +
        "								<textarea class='modal-textarea certificate-textarea'>\n" +
        "								</textarea>\n" +
        "<div style='color:#F00'></div>" +
        "\n" +
        "                                                                    <div class=\"form-inline\">\n" +
        "                                                                        <div class='form-group pull-left'>\n" +
        "                                                                            <label><span>(pem编码)</span></label>\n" +
        "                                                                            <button type='button'\n" +
        "                                                                                    class='certificate-example hidden'\n" +
        "                                                                                    onclick=''>样例参考\n" +
        "                                                                            </button>\n" +
        "                                                                        </div>\n" +
        "                                                                    </div>\n" +
        "                                                                </div>\n" +
        "                                                            </div>\n" +
        "                                                            <div class='row certificate-row'>\n" +
        "                                                                <div class='col-md-3 certificate-name'><p>*私钥</p></div>\n" +
        "                                                                <div class='col-md-8'>\n" +
        "								<textarea class='modal-textarea certificate-textarea'>\n" +
        "								</textarea>\n" +
        "<div style='color:#F00'></div>" +
        "\n" +
        "                                                                    <div class=\"form-inline\">\n" +
        "                                                                        <div class='form-group pull-left'>\n" +
        "                                                                            <label><span>(pem编码)</span></label>\n" +
        "                                                                            <button type='button'\n" +
        "                                                                                    class='certificate-example hidden'\n" +
        "                                                                                    onclick=''>样例参考\n" +
        "                                                                            </button>\n" +
        "                                                                        </div>\n" +
        "                                                                    </div>\n" +
        "                                                                </div>\n" +
        "                                                            </div>\n" +
        "                                                            <div class='form-group use-ruidun-sertificate' style='margin-left: 20px !important;'>\n" +
        "                                                                <input type='checkbox' onclick='disableTextArea(this)'>&nbsp;&nbsp;使用睿盾证书\n" +
        "                                                            </div>\n" +
        "                                                        </div>\n" +
        "                                                        <div style='color:red'> </div> "+
        "                                                        <div class='modal-footer'>\n" +
        "                                                            <button id='certificateCancel' type='button'\n" +
        "                                                                    class='btn btn-default' onclick='closeDDosModals(this, 2);'>关闭\n" +
        "                                                            </button>\n" +
        "                                                            <button id='certificateConfirm' type='button'\n" +
        "                                                                    class='btn btn-primary'\n" +
        "                                                                    onclick='saveDDosModalChanges(this, 2);'>保存\n" +
        "                                                            </button>\n" +
        "                                                        </div>\n" +
        "                                                    </div>\n" +
        "                                                </div>\n" +
        "                                            </div> <!--/modal certificate-->";

    return str;

}

/*************config*************//////
function getConfigFinish() {
    var str = " <tr class=\"config-part hidden\" id=\"finish1\">\n" +
        "                        <th><span>完成</span></th>\n" +
        "                        <td>\n" +
        "                            <div id=\"saveAllConfig\" class=\"area-config\">\n" +
        "                                <h2><span class=\"checkIcon\"></span>恭喜你，已完成所有的配置!</h2>\n" +
        "                                <ul class=\"finishConfig\">\n" +
        "                                    <li class=\"circle-li\">&nbsp;&nbsp;如您还有未完成的配置，请点击上一步，修改配置信息</li>\n" +
        "                                    <li class=\"circle-li\">&nbsp;&nbsp;如您所有配置填写完整，请点击提交订单，客服会尽快与您联系并报价</li>\n" +
        "                                    <li class=\"circle-li\">&nbsp;&nbsp;如您暂时不想提交订单，请单击保存并返回，您可在我的订单中随时提交订单</li>\n" +
        "                                </ul>\n" +
        "                                <!--<div class=\"form-group\">-->\n" +
        "                                <!--<button type=\"button\" class=\"btn btn-default\">-->\n" +
        "                                <!--<li class=\"fa fa-arrow-left\"></li>-->\n" +
        "                                <!--&nbsp;&nbsp;上一步-->\n" +
        "                                <!--</button>-->\n" +
        "                                <!--<button type=\"button\" class=\"btn btn-info\">-->\n" +
        "                                <!--<li class=\"fa fa-save\"></li>-->\n" +
        "                                <!--&nbsp;&nbsp;保存并退出-->\n" +
        "                                <!--</button>-->\n" +
        "                                <!--<button type=\"button\" class=\"btn btn-success\">-->\n" +
        "                                <!--<li class=\"fa fa-upload\"></li>-->\n" +
        "                                <!--&nbsp;&nbsp;提交订单-->\n" +
        "                                <!--</button>-->\n" +
        "                                <!--</div>-->\n" +
        "                            </div>\n" +
        "                        </td>\n" +
        "                    </tr>";
    return str;
}

function getConfigDDos() {
    var str = configDDos_1() +
        "                    <tr class=\"config-part hidden\" id=\"ddos2\">\n" +
        "                        <th><span>安全配置</span></th>\n" +
        "                        <td>\n" +
        "                            <div class=\"one-config  header-line\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>协议转发：</span>\n" +
        "                                </label>\n" +
        "                            </div>\n" +


        configDDos_2_1() +

        "\n" +
        "\n" +
        "                            <!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-->\n" +
        "\n" +
        "                            <!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-->\n" +
        "\n" +
        "                            <!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-->\n" +
        "                            <div class=\"one-config  header-line\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>网站防护：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                            </div>\n" +
        configDDos_2_2() +
        "\n" +

        "                        </td>\n" +
        "                    </tr>";
    return str;
}

function configDDos_1() {
    var str = "<tr class=\"config-part hidden\" id=\"ddos1\">\n" +
        "                        <th><span>基本配置</span></th>\n" +
        "                        <td>\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>线路:</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"btn-group config-btn-group\" role=\"group\">\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn\">中国电信</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn\">中国联通</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn\">中国移动</button>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>防护带宽：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div id=\"bandwidth-range\" class=\"config-content\">\n" +
        "                                    <input type=\"number\" min=\"0\" max=\"300\" value=\"0\" step=\"1\" id=\"input-bandwidth\">\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>购买时长：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"btn-group config-btn-group\" role=\"group\">\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">1个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">2个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">3个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">4个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">5个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">6个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">7个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">8个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">9个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">\n" +
        "                                            <li class=\"fa fa-gift gift\">&nbsp;&nbsp;</li>\n" +
        "                                            1年\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">\n" +
        "                                            <li class=\"fa fa-gift gift\">&nbsp;&nbsp;</li>\n" +
        "                                            2年\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">\n" +
        "                                            <li class=\"fa fa-gift gift\">&nbsp;&nbsp;</li>\n" +
        "                                            3年\n" +
        "                                        </button>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "\n" +
        "                            </div>\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>回源IP上限：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"dropdown\">\n" +
        "                                        <button id=\"traceBackIP\" type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                class=\"btn  btn-uplimit\"\n" +
        "                                                aria-haspopup=\"true\"\n" +
        "                                                aria-expanded=\"false\">\n" +
        "                                            <img src=\"images/ip.png\" width=\"18px;\" height=\"18px;\">\n" +
        "                                            <span>10</span>\n" +
        "                                            <span class=\"caret\"></span>\n" +
        "                                        </button>\n" +
        "                                        <ul class=\"dropdown-menu\">\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">10</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">20</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">30</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">40</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">50</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">60</li>\n" +
        "                                        </ul>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>域名上限：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"dropdown\">\n" +
        "                                        <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                class=\" btn  btn-uplimit \"\n" +
        "                                                aria-haspopup=\"true\"\n" +
        "                                                aria-expanded=\"false\">\n" +
        "                                            <img src=\"images/domain.png\" width=\"18px;\" height=\"18px;\">\n" +
        "                                            <span>10</span>\n" +
        "                                            <span class=\"caret\"></span>\n" +
        "                                        </button>\n" +
        "                                        <ul class=\"dropdown-menu\">\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">10</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">20</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">30</li>\n" +
        "                                        </ul>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>协议转发上限：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"dropdown\">\n" +
        "                                        <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                class=\"btn  btn-uplimit\"\n" +
        "                                                aria-haspopup=\"true\"\n" +
        "                                                aria-expanded=\"false\">\n" +
        "                                            <img src=\"images/protocol.png\" width=\"18px;\" height=\"18px;\">\n" +
        "                                            <span>10</span>\n" +
        "                                            <span class=\"caret\"></span>\n" +
        "                                        </button>\n" +
        "                                        <ul class=\"dropdown-menu\">\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">10</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">20</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">30</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">40</li>\n" +
        "                                        </ul>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>黑白名单上限：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"dropdown\">\n" +
        "                                        <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                class=\"btn  btn-uplimit\"\n" +
        "                                                aria-haspopup=\"true\"\n" +
        "                                                aria-expanded=\"false\">\n" +
        "                                            <img src=\"images/blackwhitelist.png\" width=\"18px;\" height=\"18px;\">\n" +
        "                                            <span id=\"namelist\">5</span>\n" +
        "                                            <span class=\"caret\"></span>\n" +
        "                                        </button>\n" +
        "                                        <ul class=\"dropdown-menu\" id=\"nameslist\">\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">5</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">10</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">20</li>\n" +
        "                                        </ul>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "\n" +
        "                        </td>\n" +
        "                    </tr>\n";
    return str;
}
function configDDos_2_1() {
    var str = "                            <div class=\"area-config\">\n" +
        "                                <table class=\"table table-striped protocol_td tbl_font_size\" id=\"tbl_proto_forward\">\n" +
        "                                    <thead class=\"thead_pad\">\n" +
        "                                    <tr>\n" +
        "                                        <th>状态</th>\n" +
        "                                        <th>线路</th>\n" +
        "                                        <th>转发协议</th>\n" +
        "                                        <th>端口</th>\n" +
        "                                        <th>源站端口</th>\n" +
        "                                        <th>黑白名单</th>\n" +
        "                                        <th>负载均衡策略</th>\n" +
        "                                        <th>源站IP</th>\n" +
        "                                        <th>CC防护</th>\n" +
        "                                        <th>操作</th>\n" +
        "                                    </tr>\n" +
        "                                    </thead>\n" +
        "                                    <tbody>\n" +
        "\n" +
        "                                    <tr>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_10_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn  btn-ddos-link\"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span id=\"ddos_farward_link\">中国电信</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\" id=\"numddosfarwardlinklist\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">中国电信</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">中国联通</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">中国移动</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>TCP</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\" id=\"protocolslist\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">UDP</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">TCP</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <input type=\"text\" placeholder=\"端口\" class=\"input_port input-sm\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\"><input type=\"text\" placeholder=\"端口\"\n" +
        "                                                                        class=\"input_port input-sm\"></td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <button class=\"btn btn-link \" data-toggle='modal'\n" +
        "                                                    data-target='#blackWhiteListModal_forward0'>配置\n" +
        "                                            </button>\n" +
        "\n" +
        "                                            <!-- Modal black-white-list -->\n" +
        "                                            <div class='modal fade' id='blackWhiteListModal_forward0' tabindex=\"-1\" role='dialog'\n" +
        "                                                 aria-labledby='#myModalLabel'>\n" +
        "                                                <div class='modal-dialog' role='document'>\n" +
        "                                                    <div class='modal-content'>\n" +
        "                                                        <div class=\"modal-header\">\n" +
        "                                                            <button type=\"button\" class=\"close\" data-dismiss=\"modal\"\n" +
        "                                                                    aria-label=\"Close\"><span\n" +
        "                                                                    aria-hidden=\"true\">&times;</span></button>\n" +
        "                                                            <h4 class=\"modal-title\" id=\"myModalLabel\">添加黑白名单</h4>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-body'>\n" +
        "                                                            <div class='pull-left'>\n" +
        "                                                                <h4><span class=\"modal-tab-color\">|</span>&nbsp;&nbsp;IP黑名单\n" +
        "                                                                </h4>\n" +
        "                                                            </div>\n" +
        "                                                            <textarea class='modal-textarea'>127.0.0.1/24</textarea>\n" +
        "\n" +
        "                                                            <div class='pull-left'>\n" +
        "                                                                <h4><span class=\"modal-tab-color\">|</span>&nbsp;&nbsp;IP白名单\n" +
        "                                                                </h4>\n" +
        "                                                            </div>\n" +
        "                                                            <textarea class='modal-textarea'>127.0.0.1/24</textarea>\n" +
        "\n" +
        "                                                            <div class='black-white-list-alert'>\n" +
        "                                                                <p>使用回车/换行分隔多个IP，支持网段添加如127.0.0.1/24，最多100个</p>\n" +
        "                                                            </div>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-footer'>\n" +
        "                                                            <button id='blackWhiteListCancel' type='button'\n" +
        "                                                                    class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                                                            </button>\n" +
        "                                                            <button id='blackWhiteListConfirm' type='button'\n" +
        "                                                                    class='btn btn-primary'\n" +
        "                                                                    onclick='saveDDosModalChanges(this);'>保存\n" +
        "                                                            </button>\n" +
        "                                                        </div>\n" +
        "                                                    </div>\n" +
        "                                                </div>\n" +
        "                                            </div>\n" +
        "\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>轮询</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\" id=\"loadbalances\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">一致性哈希</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">随机</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\"><input type=\"text\" placeholder=\"逗号隔开，最多10个\"\n" +
        "                                                                         class=\"input-sm\"></td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div>\n" +
        "                                                <input type=\"checkbox\" checked data-toggle=\"toggle\"\n" +
        "                                                       data-size=\"mini\"/>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,1);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_proto_forward','avail_proto_forward_num',1);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "\n" +
        "                                        </td>\n" +
        "                                    </tr>\n" +
        "                                    </tbody>\n" +
        "                                </table>\n" +
        "\n" +
        "                                <div class=\"add_div_border\">\n" +
        "                                    <button class=\"btn btn-link btn-sm \" id=\"btn_proto_forward\"\n" +
        "                                            onclick=\"btn_proto_add();\">\n" +
        "                                        <img width=\"20px\" height=\"20px\" src=\"images/add.png\">\n" +
        "                                        <em>添加</em>\n" +
        "                                    </button>\n" +
        "                                    <span id=\"span_avail_proto_forward_num\"> 您还可以添加<Strong id=\"avail_proto_forward_num\">9</Strong>条协议转发规则</span>\n" +
        "                                </div>\n" +
        "                            </div>\n";
    return str;
}
function configDDos_2_2() {
    var str = "                            <div class=\"area-config\">\n" +
        "                                <table class=\"table table-striped  protocol_td tbl_font_size\" id=\"tbl_website_defend\">\n" +
        "                                    <thead class=\"thead_pad\">\n" +
        "                                    <tr>\n" +
        "                                        <th>状态</th>\n" +
        "                                        <th>线路</th>\n" +
        "                                        <th>域名</th>\n" +
        "                                        <th>协议</th>\n" +
        "                                        <th>源站IP</th>\n" +
        "                                        <th>源端口</th>\n" +
        "                                        <th>负载均衡策略</th>\n" +
        "                                        <th>黑白名单</th>\n" +
        "                                        <th>CC防护</th>\n" +
        "                                        <th>操作</th>\n" +
        "                                    </tr>\n" +
        "                                    </thead>\n" +
        "                                    <tbody>\n" +
        "\n" +
        "                                    <tr>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_10_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn  btn-ddos-link\"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span id=\"ddos_defend_link\">中国电信</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\" id=\"numddosdefendlinklist\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">中国电信</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">中国联通</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">中国移动</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_13_percent\">\n" +
        "                                            <input type=\"text\" class=\"input-sm\" placeholder=\"输入域名\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_10_percent\">\n" +
        "                                            <div class=\"checkbox margin_zero\">\n" +
        "                                                <label>\n" +
        "                                                    <input type=\"radio\" name=\"protoRadios\"\n" +
        "                                                           onclick=\"protoRadiosClick(this, '', 2);\" value=\"http\"> HTTP&nbsp;&nbsp;\n" +
        "                                                </label>\n" +
        "                                            </div>\n" +
        "                                            <div class=\"checkbox margin_zero\">\n" +
        "                                                <label>\n" +
        "                                                    <input type=\"radio\" name=\"protoRadios\"\n" +
        "                                                           onclick=\"protoRadiosClick(this,'0',2);\" value=\"https\"\n" +
        "                                                            > HTTPS\n" +
        "                                                </label>\n" +
        "                                            </div>\n" +
        "\n" +
        "                                            <!-- Modal Certificate -->\n" +
        "                                            <div class='modal fade' id='uploadCertificateModal_defend0' tabindex=\"-1\"\n" +
        "                                                 role='dialog' aria-labledby='#myModalLabel'>\n" +
        "                                                <div class='modal-dialog' role='document'>\n" +
        "                                                    <div class='modal-content'>\n" +
        "                                                        <div class=\"modal-header\">\n" +
        "                                                            <button type=\"button\" class=\"close\" data-dismiss=\"modal\"\n" +
        "                                                                    aria-label=\"Close\"><span\n" +
        "                                                                    aria-hidden=\"true\">&times;</span></button>\n" +
        "                                                            <h4 class=\"modal-title\" id=\"myModalLabel1\">上传证书</h4>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-body'>\n" +
        "                                                            <div class='row certificate-row'>\n" +
        "                                                                <div class='col-md-3 certificate-name'><p>*证书内容</p>\n" +
        "                                                                </div>\n" +
        "                                                                <div class='col-md-8'>\n" +
        "								<textarea class='modal-textarea certificate-textarea'>---BEGIN CERTIFICATE---\n" +
        "									jfsldkfjiewr983274oi32j423894u3i14j3143149\n" +
        "									fjlasdkjfoeiur939329432\n" +
        "									jfoiqejuflkasjfoujeofljalkdfjldafjlkdajflk\n" +
        "									fjdsfjlksdjf8JFFOSfu9df\n" +
        "									fjdlksfjlksdfjkldsJKLFJKLJDFKFLKDFJiejf324\n" +
        "									fLJFKLfWw$853RJERJLKrFe\n" +
        "									5784ifjsirwefdsfsdnkfsdfjwe8hFt9eijfkdjfoe\n" +
        "									vnshdkfheiowureiRW#RIUk\n" +
        "								</textarea>\n" +
        "\n" +
        "                                                                    <div class=\"form-inline\">\n" +
        "                                                                        <div class='form-group pull-left'>\n" +
        "                                                                            <label><span class=\"pemcode\">(pem编码)</span></label>\n" +
        "                                                                            <button type='button'\n" +
        "                                                                                    class='certificate-example'\n" +
        "                                                                                    onclick=''>样例参考\n" +
        "                                                                            </button>\n" +
        "                                                                        </div>\n" +
        "                                                                    </div>\n" +
        "                                                                </div>\n" +
        "                                                            </div>\n" +
        "                                                            <div class='row certificate-row'>\n" +
        "                                                                <div class='col-md-3 certificate-name'><p>*私钥</p></div>\n" +
        "                                                                <div class='col-md-8'>\n" +
        "								<textarea class='modal-textarea certificate-textarea'>---BEGIN RSA PRIVATE KEY---\n" +
        "									jfsldkfFfier983274oi32j423894u3i14j3143149\n" +
        "									fjlasdkjfoeiur939329432\n" +
        "									jfoiqejuflkasjfoujeofljalkdfjldafjlkdajflk\n" +
        "									fjdsfjlksdjf8JFFOSfu9df\n" +
        "									fjdlksfjlksdfjkldsJKLFJKLJDFKFLKDFJiejf324\n" +
        "									fLJFKLfWw$853RJERJLKrFe\n" +
        "								</textarea>\n" +
        "\n" +
        "                                                                    <div class=\"form-inline\">\n" +
        "                                                                        <div class='form-group pull-left'>\n" +
        "                                                                            <label><span class=\"pemcode\">(pem编码)</span></label>\n" +
        "                                                                            <button type='button'\n" +
        "                                                                                    class='certificate-example'\n" +
        "                                                                                    onclick=''>样例参考\n" +
        "                                                                            </button>\n" +
        "                                                                        </div>\n" +
        "                                                                    </div>\n" +
        "                                                                </div>\n" +
        "                                                            </div>\n" +
        "                                                            <div class='form-group use-ruidun-sertificate'>\n" +
        "                                                                <input type='checkbox'>&nbsp;&nbsp;使用睿盾证书\n" +
        "                                                            </div>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-footer'>\n" +
        "                                                            <button id='certificateCancel' type='button'\n" +
        "                                                                    class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                                                            </button>\n" +
        "                                                            <button id='certificateConfirm' type='button'\n" +
        "                                                                    class='btn btn-primary'\n" +
        "                                                                    onclick='saveDDosModalChanges(this);'>保存\n" +
        "                                                            </button>\n" +
        "                                                        </div>\n" +
        "                                                    </div>\n" +
        "                                                </div>\n" +
        "                                            </div> <!--/modal certificate-->\n" +
        "\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_13_percent\"><input type=\"text\" value=\"123.231.32.123\" class=\"input-sm\"></td>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <span>443</span>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>轮询</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">一致性哈希</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this)\">随机</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <button class=\"btn btn-link\" data-toggle='modal'\n" +
        "                                                    data-target='#blackWhiteListModal_defend0'>配置\n" +
        "                                            </button>\n" +
        "\n" +
        "                                            <!-- Modal black-white-list -->\n" +
        "                                            <div class='modal fade' id='blackWhiteListModal_defend0' tabindex=\"-1\"\n" +
        "                                                 role='dialog'\n" +
        "                                                 aria-labledby='#myModalLabel'>\n" +
        "                                                <div class='modal-dialog' role='document'>\n" +
        "                                                    <div class='modal-content'>\n" +
        "                                                        <div class=\"modal-header\">\n" +
        "                                                            <button type=\"button\" class=\"close\" data-dismiss=\"modal\"\n" +
        "                                                                    aria-label=\"Close\"><span\n" +
        "                                                                    aria-hidden=\"true\">&times;</span></button>\n" +
        "                                                            <h4 class=\"modal-title\">添加黑白名单</h4>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-body'>\n" +
        "                                                            <div class='pull-left'>\n" +
        "                                                                <h4><span class=\"modal-tab-color\">|</span>&nbsp;&nbsp;IP黑名单\n" +
        "                                                                </h4>\n" +
        "                                                            </div>\n" +
        "                                                            <textarea class='modal-textarea'>127.0.0.1/24</textarea>\n" +
        "\n" +
        "                                                            <div class='pull-left'>\n" +
        "                                                                <h4><span class=\"modal-tab-color\">|</span>&nbsp;&nbsp;IP白名单\n" +
        "                                                                </h4>\n" +
        "                                                            </div>\n" +
        "                                                            <textarea class='modal-textarea'>127.0.0.1/24</textarea>\n" +
        "\n" +
        "                                                            <div class='black-white-list-alert'>\n" +
        "                                                                <p>使用回车/换行分隔多个IP，支持网段添加如127.0.0.1/24，最多100个</p>\n" +
        "                                                            </div>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-footer'>\n" +
        "                                                            <button type='button'\n" +
        "                                                                    class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                                                            </button>\n" +
        "                                                            <button type='button'\n" +
        "                                                                    class='btn btn-primary'\n" +
        "                                                                    onclick='saveDDosModalChanges(this);'>保存\n" +
        "                                                            </button>\n" +
        "                                                        </div>\n" +
        "                                                    </div>\n" +
        "                                                </div>\n" +
        "                                            </div>\n" +
        "\n" +
        "\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div>\n" +
        "                                                <input type=\"checkbox\" checked data-toggle=\"toggle\" data-size=\"mini\"/>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_website_defend','avail_website_defend_num',2);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "                                    </tr>\n" +
        "\n" +
        "\n" +
        "                                    </tbody>\n" +
        "                                </table>\n" +
        "                                <div class=\"add_div_border\">\n" +
        "                                    <button class=\"btn btn-link btn-sm\" onclick=\"btn_website_defend_add();\"\n" +
        "                                            id=\"btn_website_defend_add\">\n" +
        "                                        <img width=\"20px\" height=\"20px\" src=\"images/add.png\">\n" +
        "                                        <em>添加</em>\n" +
        "                                    </button>\n" +
        "                                    <span id=\"span_website_defend_num\">\n" +
        "                                        您还可以添加<Strong id=\"avail_website_defend_num\">9</Strong>个域名\n" +
        "                                    </span>\n" +
        "                                </div>\n" +
        "                            </div>\n";
    return str;
}

function getConfigCDN() {
    var str = "<tr class=\"config-part hidden\" id=\"cdn1\">\n" +
        "                        <th><span>基本配置</span></th>\n" +
        configCDN_1() +
        "                    </tr>\n" +
        "\n" +
        "\n" +
        "                    <tr class=\"config-part hidden\" id=\"cdn2\">\n" +
        "                        <th><span>域名接入</span></th>\n" +
        configCDN_2() +
        "                    </tr>\n" +
        "                    <tr class=\"config-part hidden\" id=\"cdn3\">\n" +
        "                        <th><span>加速配置</span></th>\n" +
        configCDN_3() +
        "                    </tr>";
    return str;
}

function configCDN_1() {
    var str = "                   <td>\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>业务类型:</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"btn-group config-btn-group\" role=\"group\">\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn-business-type config-cdn-business\">\n" +
        "                                            静态页面、小文件加速\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn-business-type\">动态加速</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn-business-type\">大文件下载加速</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn-business-type\">视频点播加速</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn-business-type\">直播加速</button>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>加速线路:</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"btn-group config-btn-group\" role=\"group\">\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn\">中国电信</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn\">中国联通</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn\">中国移动</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn\">教育网</button>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>回源IP上限：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"dropdown\">\n" +
        "                                        <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                class=\"btn  btn-uplimit\"\n" +
        "                                                aria-haspopup=\"true\"\n" +
        "                                                aria-expanded=\"false\">\n" +
        "                                            <img src=\"images/ip.png\" width=\"18px;\" height=\"18px;\">\n" +
        "                                            <span id=\"cdn_numOfIps\">10</span>\n" +
        "                                            <span class=\"caret\"></span>\n" +
        "                                        </button>\n" +
        "                                        <ul class=\"dropdown-menu\" id=\"ipslist\">\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">10</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">20</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">30</li>\n" +
        "                                        </ul>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>缓存配置上限：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"dropdown\">\n" +
        "                                        <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                class=\" btn  btn-uplimit \"\n" +
        "                                                aria-haspopup=\"true\"\n" +
        "                                                aria-expanded=\"false\">\n" +
        "                                            <img src=\"images/cache-data.png\" width=\"18px;\" height=\"18px;\">\n" +
        "                                            <span id=\"cdn_numcacheconfig\">10</span>\n" +
        "                                            <span class=\"caret\"></span>\n" +
        "                                        </button>\n" +
        "                                        <ul class=\"dropdown-menu\" id=\"domainslist\">\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">10</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">20</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">30</li>\n" +
        "                                        </ul>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>购买时长：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"btn-group config-btn-group\" role=\"group\">\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">1个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">2个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">3个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">4个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">5个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">6个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">7个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">8个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">9个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">\n" +
        "                                            <li class=\"fa fa-gift gift\">&nbsp;&nbsp;</li>\n" +
        "                                            1年\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">\n" +
        "                                            <li class=\"fa fa-gift gift\">&nbsp;&nbsp;</li>\n" +
        "                                            2年\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">\n" +
        "                                            <li class=\"fa fa-gift gift\">&nbsp;&nbsp;</li>\n" +
        "                                            3年\n" +
        "                                        </button>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "\n" +
        "                            </div>\n" +
        "                        </td>\n";
    return str;
}
function configCDN_2() {
    var str = "                   <td>\n" +
        "                            <div class=\"area-config\">\n" +
        "                                <table class=\"table table-striped  protocol_td tbl_font_size\">\n" +
        "                                    <thead class=\"thead_pad\">\n" +
        "                                    <tr>\n" +
        "                                        <th>状态</th>\n" +
        "                                        <th>加速域名</th>\n" +
        "                                        <th>协议</th>\n" +
        "                                        <th>证书</th>\n" +
        "                                        <th>回源方式</th>\n" +
        "                                        <th>源站域名/IP</th>\n" +
        "                                        <th>操作</th>\n" +
        "                                    </tr>\n" +
        "                                    </thead>\n" +
        "                                    <tbody>\n" +
        "\n" +
        "                                    <tr>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <label class=\"label label-primary\" style=\"font-size: 18px;\">\n" +
        "                                                <span>image.a.com</span>\n" +
        "                                            </label>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "\n" +
        "                                            <div class=\"checkbox \">\n" +
        "                                                <label>\n" +
        "                                                    <input type=\"checkbox\" onclick=\"protoCheckBoxClick(this);\" value=\"http\"> HTTP&nbsp;&nbsp;\n" +
        "                                                </label>\n" +
        "                                            </div>\n" +
        "                                            <div class=\"checkbox\">\n" +
        "                                                <label>\n" +
        "                                                    <input type=\"checkbox\" onclick=\"protoCheckBoxClick(this, 'uploadCertificateModal_cdn0');\" value=\"https\"> HTTPS\n" +
        "                                                </label>\n" +
        "                                            </div>\n" +
        "                                            <!-- Modal Certificate -->\n" +
        "                                            <div class='modal fade' id='uploadCertificateModal_cdn0' tabindex=\"-1\"\n" +
        "                                                 role='dialog' aria-labledby='#myModalLabel'>\n" +
        "                                                <div class='modal-dialog' role='document'>\n" +
        "                                                    <div class='modal-content'>\n" +
        "                                                        <div class=\"modal-header\">\n" +
        "                                                            <button type=\"button\" class=\"close\" data-dismiss=\"modal\"\n" +
        "                                                                    aria-label=\"Close\"><span\n" +
        "                                                                    aria-hidden=\"true\">&times;</span></button>\n" +
        "                                                            <h4 class=\"modal-title\" id=\"myModalLabel1\">上传证书</h4>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-body'>\n" +
        "                                                            <div class='row certificate-row'>\n" +
        "                                                                <div class='col-md-3 certificate-name'><p>*证书内容</p>\n" +
        "                                                                </div>\n" +
        "                                                                <div class='col-md-8'>\n" +
        "								<textarea class='modal-textarea certificate-textarea'>---BEGIN CERTIFICATE---\n" +
        "									jfsldkfjiewr983274oi32j423894u3i14j3143149\n" +
        "									fjlasdkjfoeiur939329432\n" +
        "									jfoiqejuflkasjfoujeofljalkdfjldafjlkdajflk\n" +
        "									fjdsfjlksdjf8JFFOSfu9df\n" +
        "									fjdlksfjlksdfjkldsJKLFJKLJDFKFLKDFJiejf324\n" +
        "									fLJFKLfWw$853RJERJLKrFe\n" +
        "									5784ifjsirwefdsfsdnkfsdfjwe8hFt9eijfkdjfoe\n" +
        "									vnshdkfheiowureiRW#RIUk\n" +
        "								</textarea>\n" +
        "\n" +
        "                                                                    <div class=\"form-inline\">\n" +
        "                                                                        <div class='form-group pull-left'>\n" +
        "                                                                            <label><span class=\"pemcode\">(pem编码)</span></label>\n" +
        "                                                                            <button type='button'\n" +
        "                                                                                    class='certificate-example'\n" +
        "                                                                                    onclick=''>样例参考\n" +
        "                                                                            </button>\n" +
        "                                                                        </div>\n" +
        "                                                                    </div>\n" +
        "                                                                </div>\n" +
        "                                                            </div>\n" +
        "                                                            <div class='row certificate-row'>\n" +
        "                                                                <div class='col-md-3 certificate-name'><p>*私钥</p></div>\n" +
        "                                                                <div class='col-md-8'>\n" +
        "								<textarea class='modal-textarea certificate-textarea'>---BEGIN RSA PRIVATE KEY---\n" +
        "									jfsldkfFfier983274oi32j423894u3i14j3143149\n" +
        "									fjlasdkjfoeiur939329432\n" +
        "									jfoiqejuflkasjfoujeofljalkdfjldafjlkdajflk\n" +
        "									fjdsfjlksdjf8JFFOSfu9df\n" +
        "									fjdlksfjlksdfjkldsJKLFJKLJDFKFLKDFJiejf324\n" +
        "									fLJFKLfWw$853RJERJLKrFe\n" +
        "								</textarea>\n" +
        "\n" +
        "                                                                    <div class=\"form-inline\">\n" +
        "                                                                        <div class='form-group pull-left'>\n" +
        "                                                                            <label><span class=\"pemcode\">(pem编码)</span></label>\n" +
        "                                                                            <button type='button'\n" +
        "                                                                                    class='certificate-example'\n" +
        "                                                                                    onclick=''>样例参考\n" +
        "                                                                            </button>\n" +
        "                                                                        </div>\n" +
        "                                                                    </div>\n" +
        "                                                                </div>\n" +
        "                                                            </div>\n" +
        "                                                            <div class='form-group use-ruidun-sertificate'>\n" +
        "                                                                <input type='checkbox'>&nbsp;&nbsp;使用睿盾证书\n" +
        "                                                            </div>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-footer'>\n" +
        "                                                            <button id='certificateCancel' type='button'\n" +
        "                                                                    class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                                                            </button>\n" +
        "                                                            <button id='certificateConfirm' type='button'\n" +
        "                                                                    class='btn btn-primary'\n" +
        "                                                                    onclick='saveDDosModalChanges(this);'>保存\n" +
        "                                                            </button>\n" +
        "                                                        </div>\n" +
        "                                                    </div>\n" +
        "                                                </div>\n" +
        "                                            </div> <!--/modal certificate-->\n" +
        "\n" +
        "\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <img src=\"images/before_config.png\" width=\"20px\" height=\"20px\">\n" +
        "\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_15_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>域名</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">IP</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this)\">域名</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <input type=\"text\" class=\"input-sm\" placeholder=\"输入源站域名或者IP\">\n" +
        "                                        </td>\n" +
        "\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_website_defend','avail_website_defend_num',2);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "\n" +
        "                                    </tr>\n" +
        "                                    </tbody>\n" +
        "                                </table>\n" +
        "\n" +
        "                            </div>\n" +
        "\n" +
        "                        </td>\n";
    return str;
}
function configCDN_3() {
    var str = "                        <td>\n" +
        "\n" +
        "                            <div class=\"one-config  header-line\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>缓存配置：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                            </div>\n" +
        "\n" +
        "\n" +
        "                            <div class=\"area-config\">\n" +
        "                                <table class=\"table table-striped protocol_td tbl_font_size\" id=\"tbl_rules_config\">\n" +
        "                                    <thead class=\"thead_pad\">\n" +
        "                                    <tr>\n" +
        "                                        <th>状态</th>\n" +
        "                                        <th>类型</th>\n" +
        "                                        <th>内容</th>\n" +
        "                                        <th>过期时间</th>\n" +
        "                                        <th>权重</th>\n" +
        "                                        <th>操作</th>\n" +
        "\n" +
        "                                    </tr>\n" +
        "                                    </thead>\n" +
        "                                    <tbody>\n" +
        "                                    <tr>\n" +
        "\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_13_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>后缀名</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">后缀名</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this)\">目录</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <input type=\"text\" class=\"input-sm\" placeholder=\"输入后缀,例如:js/css\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <div class=\"input-group\" style=\"width: 175px;\">\n" +
        "                                                <input type=\"text\" class=\"form-control\"\n" +
        "                                                       style=\"width: 60px;float: right;\">\n" +
        "\n" +
        "                                                <div class=\"input-group-btn\">\n" +
        "                                                    <button type=\"button\" class=\"btn btn-default dropdown-toggle\"\n" +
        "                                                            data-toggle=\"dropdown\" aria-haspopup=\"true\"\n" +
        "                                                            aria-expanded=\"false\">\n" +
        "                                                        <span>小时</span>\n" +
        "                                                        <span class=\"caret\"></span>\n" +
        "                                                    </button>\n" +
        "                                                    <ul class=\"dropdown-menu dropdown-menu-right\">\n" +
        "\n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">分钟</li>\n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">小时</li>\n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">&nbsp;&nbsp;&nbsp;天</li>\n" +
        "                                                    </ul>\n" +
        "                                                </div>\n" +
        "                                                <!-- /btn-group -->\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <input type=\"text\" placeholder=\"权重\"\n" +
        "                                                   class=\"input-sm\" style=\"width: 50px !important;\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_rules_config','avail_rules_num',3);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "                                    </tr>\n" +
        "                                    <tr>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_13_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>后缀名</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">后缀名</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this)\">目录</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <input type=\"text\" class=\"input-sm\" placeholder=\"输入目录,例如:/wwww、/a\">\n" +
        "                                        </td>\n" +
        "\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "\n" +
        "                                            <div class=\"input-group\" style=\"width: 175px;\">\n" +
        "                                                <input type=\"text\" class=\"form-control\"\n" +
        "                                                       style=\"width: 60px;float: right;\">\n" +
        "\n" +
        "                                                <div class=\"input-group-btn\">\n" +
        "                                                    <button type=\"button\" class=\"btn btn-default dropdown-toggle\"\n" +
        "                                                            data-toggle=\"dropdown\" aria-haspopup=\"true\"\n" +
        "                                                            aria-expanded=\"false\">\n" +
        "                                                        <span>小时</span>\n" +
        "                                                        <span class=\"caret\"></span>\n" +
        "                                                    </button>\n" +
        "                                                    <ul class=\"dropdown-menu dropdown-menu-right\">\n" +
        "\n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">分钟</li>\n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">小时</li>\n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">&nbsp;&nbsp;&nbsp;天</li>\n" +
        "                                                    </ul>\n" +
        "                                                </div>\n" +
        "                                                <!-- /btn-group -->\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <input type=\"text\" placeholder=\"权重\"\n" +
        "                                                   class=\"input-sm\" style=\"width: 50px !important;\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_rules_config','avail_rules_num',3);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "\n" +
        "                                    </tr>\n" +
        "                                    </tbody>\n" +
        "                                </table>\n" +
        "                                <div class=\"add_div_border\">\n" +
        "                                    <button class=\"btn btn-link btn-sm\" onclick=\"btn_rule_add();\"\n" +
        "                                            id=\"btn_rules_add\">\n" +
        "                                        <img width=\"20px\" height=\"20px\" src=\"images/add.png\">\n" +
        "                                        <em>添加</em>\n" +
        "                                    </button>\n" +
        "                                    <span id=\"span_rules_num\">\n" +
        "                                        您还可以添加<Strong id=\"avail_rules_num\">28</Strong>条规则\n" +
        "                                    </span>\n" +
        "                                </div>\n" +
        "\n" +
        "                                <div class=\"row row-cdn\">\n" +
        "                                    <div class=\"col-md-3 \">\n" +
        "                                        <label class=\"config-name-lg\">\n" +
        "                                        <span>\n" +
        "                                            页面优化\n" +
        "                                            <img onmouseover=\"imgOnMouseOver(this)\" src=\"images/question.png\"\n" +
        "                                                 onmouseout=\"imgOnMouseOut(this)\"\n" +
        "                                                 height=\"15px\" width=\"15px\">:\n" +
        "\n" +
        "                                        </span>\n" +
        "                                        </label>\n" +
        "\n" +
        "                                    </div>\n" +
        "                                    <div class=\"col-md-3 col-md-pull-2\">\n" +
        "                                        <input type=\"checkbox\" checked data-toggle=\"toggle\" data-size=\"mini\"/>\n" +
        "                                    </div>\n" +
        "\n" +
        "                                    <div class=\"col-md-3 \">\n" +
        "                                        <label class=\"config-name-lg \">\n" +
        "                                        <span>\n" +
        "                                            智能压缩\n" +
        "                                            <img onmouseover=\"imgOnMouseOver(this)\" src=\"images/question.png\"\n" +
        "                                                 onmouseout=\"imgOnMouseOut(this)\"\n" +
        "                                                 height=\"15px\" width=\"15px\">:\n" +
        "                                        </span>\n" +
        "                                        </label>\n" +
        "                                    </div>\n" +
        "                                    <div class=\"col-md-3 col-md-pull-2\">\n" +
        "                                        <input type=\"checkbox\" checked data-toggle=\"toggle\" data-size=\"mini\"/>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                                <div class=\"row row-cdn\">\n" +
        "                                    <div class=\"col-md-3\">\n" +
        "\n" +
        "                                        <label class=\"config-name-lg \">\n" +
        "                                        <span>\n" +
        "                                            过滤参数\n" +
        "                                            <img onmouseover=\"imgOnMouseOver(this)\" src=\"images/question.png\"\n" +
        "                                                 onmouseout=\"imgOnMouseOut(this)\"\n" +
        "                                                 height=\"15px\" width=\"15px\">:\n" +
        "\n" +
        "                                        </span>\n" +
        "                                        </label>\n" +
        "                                    </div>\n" +
        "\n" +
        "                                    <div class=\"col-md-3 padding_zero col-md-pull-2\">\n" +
        "                                        <button class=\"btn btn-link\"\n" +
        "                                                onclick=\"showConfigshowModal('#filterParaConfigModal');\">\n" +
        "                                            <img src=\"images/edit.png\" width=\"18px\" height=\"18px\"\n" +
        "                                                 style=\"margin-bottom: 5px !important;\">&nbsp;设置\n" +
        "                                        </button>\n" +
        "                                    </div>\n" +
        "\n" +
        "\n" +
        "\n" +
        "                                    <div class=\"col-md-3\">\n" +
        "                                        <label class=\"config-name-lg \">\n" +
        "                                        <span>\n" +
        "                                            回源Host\n" +
        "                                            <img onmouseover=\"imgOnMouseOver(this)\" src=\"images/question.png\"\n" +
        "                                                 onmouseout=\"imgOnMouseOut(this)\"\n" +
        "                                                 height=\"15px\" width=\"15px\">:\n" +
        "\n" +
        "                                        </span>\n" +
        "                                        </label>\n" +
        "                                    </div>\n" +
        "\n" +
        "                                    <div class=\"col-md-3  col-md-pull-2 padding_zero\">\n" +
        "                                        <button class=\"btn btn-link\"\n" +
        "                                                onclick=\"showConfigshowModal('#loopSourceHostConfigModal');\">\n" +
        "                                            <img src=\"images/edit.png\" width=\"18px\" height=\"18px\"\n" +
        "                                                 style=\"margin-bottom: 5px !important;\">&nbsp;设置\n" +
        "                                        </button>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                                <div class=\"row row-cdn\">\n" +
        "\n" +
        "\n" +
        "                                    <div class=\"col-md-3\">\n" +
        "                                        <label class=\"config-name-lg \">\n" +
        "                                        <span>\n" +
        "                                            自定义404\n" +
        "                                            <img onmouseover=\"imgOnMouseOver(this)\" src=\"images/question.png\"\n" +
        "                                                 onmouseout=\"imgOnMouseOut(this)\"\n" +
        "                                                 height=\"15px\" width=\"15px\">:\n" +
        "\n" +
        "                                        </span>\n" +
        "                                        </label>\n" +
        "                                    </div>\n" +
        "\n" +
        "                                    <div class=\"col-md-3 padding_zero col-md-pull-2\">\n" +
        "                                        <button class=\"btn btn-link\"\n" +
        "                                                onclick=\"showConfigshowModal('#custom404PageConfig1Modal');\">\n" +
        "                                            <img src=\"images/edit.png\" width=\"18px\" height=\"18px\"\n" +
        "                                                 style=\"margin-bottom: 5px !important;\">&nbsp;设置\n" +
        "                                        </button>\n" +
        "                                    </div>\n" +
        "\n" +
        "\n" +
        "                                    <div class=\"col-md-3\">\n" +
        "                                        <label class=\"config-name-lg \">\n" +
        "                                        <span>\n" +
        "                                            防盗链\n" +
        "                                            <img onmouseover=\"imgOnMouseOver(this)\" src=\"images/question.png\"\n" +
        "                                                 onmouseout=\"imgOnMouseOut(this)\"\n" +
        "                                                 height=\"15px\" width=\"15px\">:\n" +
        "\n" +
        "                                        </span>\n" +
        "                                        </label>\n" +
        "                                    </div>\n" +
        "\n" +
        "                                    <div class=\"col-md-3 col-md-pull-2 padding_zero\">\n" +
        "                                        <button class=\"btn btn-link\"\n" +
        "                                                onclick=\"showConfigshowModal('#antiStealingLinkModal');\">\n" +
        "                                            <img src=\"images/edit.png\" width=\"18px\" height=\"18px\"\n" +
        "                                                 style=\"margin-bottom: 5px !important;\">&nbsp;设置\n" +
        "                                        </button>\n" +
        "                                    </div>\n" +
        "                                </div>";
    "                            </div>\n" +
    "                        </td>\n";
    return str;
}

function getConfigWaf() {
    var str = "<tr class=\"config-part hidden\" id=\"waf1\">\n" +
        "                        <th><span>基本配置</span></th>\n" +
        configWAF_1() +
        "                    </tr>\n" +
        "                    <tr class=\"config-part hidden\" id=\"waf2\">\n" +
        "                        <th><span>安全配置</span></th>\n" +
        configWAF_2() +
        "                    </tr>";
    return str;
}


function configWAF_1() {
    var str = "                        <td>\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>线路:</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"btn-group config-btn-group\" role=\"group\">\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn\">中国电信</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn\">中国联通</button>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>防护能力：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-content\">\n" +
        "                                    <div class=\"btn-group config-btn-group\" role=\"group\">\n" +
        "                                        <button type=\"button\" class=\"btn btn-default config-btn-band  config-waf-trfc\">\n" +
        "                                            1万QPS+50Mbps\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-btn-band  config-waf-trfc\">\n" +
        "                                            2万QPS+200Mbps\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-btn-band config-waf-trfc\">\n" +
        "                                            10万QPS+1Gbps\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default   config-btn-band config-waf-trfc\">\n" +
        "                                            50万QPS+5Gbps\n" +
        "                                        </button>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>访问控制规则上限：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-waf-uplimit\">\n" +
        "                                    <div class=\"dropdown\">\n" +
        "                                        <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                class=\"btn  btn-uplimit\"\n" +
        "                                                aria-haspopup=\"true\"\n" +
        "                                                aria-expanded=\"false\">\n" +
        "                                            <img src=\"images/acl.png\" width=\"18px;\" height=\"18px;\">\n" +
        "                                            <span id=\"waf_numprotocols\">100</span>\n" +
        "                                            <span class=\"caret\"></span>\n" +
        "                                        </button>\n" +
        "                                        <ul class=\"dropdown-menu\" id=\"ipslist\">\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">100</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">110</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">120</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">130</li>\n" +
        "                                        </ul>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>防护域名个数上限：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-waf-uplimit\">\n" +
        "                                    <div class=\"dropdown\">\n" +
        "                                        <button id=\"traceBackDN\" type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                class=\" btn  btn-uplimit \"\n" +
        "                                                aria-haspopup=\"true\"\n" +
        "                                                aria-expanded=\"false\">\n" +
        "                                            <img src=\"images/domain.png\" width=\"18px;\" height=\"18px;\">\n" +
        "                                            <span id=\"waf_numOfDns\">10</span>\n" +
        "                                            <span class=\"caret\"></span>\n" +
        "                                        </button>\n" +
        "                                        <ul class=\"dropdown-menu\" id=\"domainslist\">\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">10</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">20</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">30</li>\n" +
        "                                        </ul>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>回源IP个数上限：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-waf-uplimit\">\n" +
        "                                    <div class=\"dropdown\">\n" +
        "                                        <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                class=\"btn  btn-uplimit\"\n" +
        "                                                aria-haspopup=\"true\"\n" +
        "                                                aria-expanded=\"false\">\n" +
        "                                            <img src=\"images/ip.png\" width=\"18px;\" height=\"18px;\">\n" +
        "                                            <span id=\"waf_numOfIps\">10</span>\n" +
        "                                            <span class=\"caret\"></span>\n" +
        "                                        </button>\n" +
        "                                        <ul class=\"dropdown-menu\" id=\"numprotocolslist\">\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">10</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">20</li>\n" +
        "                                            <li onclick=\"selectProtoFwd(this);\">30</li>\n" +
        "                                        </ul>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "\n" +
        "                            <div class=\"one-config\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>购买时长：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                                <div class=\"config-waf-uplimit\">\n" +
        "                                    <div class=\"btn-group config-btn-group\" role=\"group\">\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">1个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">2个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">3个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">4个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">5个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">6个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">7个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">8个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">9个月</button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">\n" +
        "                                            <li class=\"fa fa-gift gift\">&nbsp;&nbsp;</li>\n" +
        "                                            1年\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">\n" +
        "                                            <li class=\"fa fa-gift gift\">&nbsp;&nbsp;</li>\n" +
        "                                            2年\n" +
        "                                        </button>\n" +
        "                                        <button type=\"button\" class=\"btn btn-default  config-times\">\n" +
        "                                            <li class=\"fa fa-gift gift\">&nbsp;&nbsp;</li>\n" +
        "                                            3年\n" +
        "                                        </button>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "\n" +
        "                            </div>\n" +
        "                        </td>\n";
    return str;
}
function configWAF_2() {
    var str = "                        <td>\n" +
        "\n" +
        "                            <!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-->\n" +
        "\n" +
        "                            <!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-->\n" +
        "\n" +
        "                            <!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!-->\n" +
        "                            <div class=\"one-config  header-line\">\n" +
        "                                <label class=\"config-name\">\n" +
        "                                    <span>WAF网站防护：</span>\n" +
        "                                </label>\n" +
        "\n" +
        "                            </div>\n" +
        "\n" +
        "\n" +
        "                            <div class=\"area-config\">\n" +
        "                                <table class=\"table table-striped  protocol_td tbl_font_size\" id=\"tbl_waf_defend\">\n" +
        "                                    <thead class=\"thead_pad\">\n" +
        "                                    <tr>\n" +
        "                                        <th>状态</th>\n" +
        "                                        <th>域名</th>\n" +
        "                                        <th>协议</th>\n" +
        "                                        <th>源站IP</th>\n" +
        "                                        <th>源端口</th>\n" +
        "                                        <th>负载均衡策略</th>\n" +
        "                                        <th>精准访问规则控制</th>\n" +
        "                                        <th>CC防护</th>\n" +
        "                                        <th>操作</th>\n" +
        "                                    </tr>\n" +
        "                                    </thead>\n" +
        "                                    <tbody>\n" +
        "\n" +
        "                                    <tr>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <input type=\"text\" class=\"input-sm\" placeholder=\"输入域名\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "\n" +
        "\n" +
        "                                            <div class=\"checkbox margin_zero\">\n" +
        "                                                <label>\n" +
        "                                                    <input type=\"radio\" name=\"protoRadios\"\n" +
        "                                                           onclick=\"protoRadiosClick(this,'',3);\" value=\"http\"> HTTP&nbsp;&nbsp;\n" +
        "                                                </label>\n" +
        "                                            </div>\n" +
        "                                            <div class=\"checkbox margin_zero\">\n" +
        "                                                <label>\n" +
        "                                                    <input type=\"radio\" name=\"protoRadios\"\n" +
        "                                                           onclick=\"protoRadiosClick(this,0,3);\" value=\"https\"\n" +
        "                                                            > HTTPS\n" +
        "                                                </label>\n" +
        "                                            </div>\n" +
        "\n" +
        "                                            <!-- Modal Certificate -->\n" +
        "                                            <div class='modal fade' id='uploadCertificateModal_waf0' tabindex=\"-1\"\n" +
        "                                                 role='dialog' aria-labledby='#myModalLabel'>\n" +
        "                                                <div class='modal-dialog' role='document'>\n" +
        "                                                    <div class='modal-content'>\n" +
        "                                                        <div class=\"modal-header\">\n" +
        "                                                            <button type=\"button\" class=\"close\" data-dismiss=\"modal\"\n" +
        "                                                                    aria-label=\"Close\"><span\n" +
        "                                                                    aria-hidden=\"true\">&times;</span></button>\n" +
        "                                                            <h4 class=\"modal-title\" id=\"myModalLabel1\">上传证书</h4>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-body'>\n" +
        "                                                            <div class='row certificate-row'>\n" +
        "                                                                <div class='col-md-3 certificate-name'><p>*证书内容</p>\n" +
        "                                                                </div>\n" +
        "                                                                <div class='col-md-8'>\n" +
        "								<textarea class='modal-textarea certificate-textarea'>---BEGIN CERTIFICATE---\n" +
        "									jfsldkfjiewr983274oi32j423894u3i14j3143149\n" +
        "									fjlasdkjfoeiur939329432\n" +
        "									jfoiqejuflkasjfoujeofljalkdfjldafjlkdajflk\n" +
        "									fjdsfjlksdjf8JFFOSfu9df\n" +
        "									fjdlksfjlksdfjkldsJKLFJKLJDFKFLKDFJiejf324\n" +
        "									fLJFKLfWw$853RJERJLKrFe\n" +
        "									5784ifjsirwefdsfsdnkfsdfjwe8hFt9eijfkdjfoe\n" +
        "									vnshdkfheiowureiRW#RIUk\n" +
        "								</textarea>\n" +
        "\n" +
        "                                                                    <div class=\"form-inline\">\n" +
        "                                                                        <div class='form-group pull-left'>\n" +
        "                                                                            <label><span class=\"pemcode\">(pem编码)</span></label>\n" +
        "                                                                            <button type='button'\n" +
        "                                                                                    class='certificate-example'\n" +
        "                                                                                    onclick=''>样例参考\n" +
        "                                                                            </button>\n" +
        "                                                                        </div>\n" +
        "                                                                    </div>\n" +
        "                                                                </div>\n" +
        "                                                            </div>\n" +
        "                                                            <div class='row certificate-row'>\n" +
        "                                                                <div class='col-md-3 certificate-name'><p>*私钥</p></div>\n" +
        "                                                                <div class='col-md-8'>\n" +
        "								<textarea class='modal-textarea certificate-textarea'>---BEGIN RSA PRIVATE KEY---\n" +
        "									jfsldkfFfier983274oi32j423894u3i14j3143149\n" +
        "									fjlasdkjfoeiur939329432\n" +
        "									jfoiqejuflkasjfoujeofljalkdfjldafjlkdajflk\n" +
        "									fjdsfjlksdjf8JFFOSfu9df\n" +
        "									fjdlksfjlksdfjkldsJKLFJKLJDFKFLKDFJiejf324\n" +
        "									fLJFKLfWw$853RJERJLKrFe\n" +
        "								</textarea>\n" +
        "\n" +
        "                                                                    <div class=\"form-inline\">\n" +
        "                                                                        <div class='form-group pull-left'>\n" +
        "                                                                            <label><span class=\"pemcode\">(pem编码)</span></label>\n" +
        "                                                                            <button type='button'\n" +
        "                                                                                    class='certificate-example'\n" +
        "                                                                                    onclick=''>样例参考\n" +
        "                                                                            </button>\n" +
        "                                                                        </div>\n" +
        "                                                                    </div>\n" +
        "                                                                </div>\n" +
        "                                                            </div>\n" +
        "                                                            <div class='form-group use-ruidun-sertificate'>\n" +
        "                                                                <input type='checkbox'>&nbsp;&nbsp;使用睿盾证书\n" +
        "                                                            </div>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-footer'>\n" +
        "                                                            <button id='certificateCancel' type='button'\n" +
        "                                                                    class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                                                            </button>\n" +
        "                                                            <button id='certificateConfirm' type='button'\n" +
        "                                                                    class='btn btn-primary'\n" +
        "                                                                    onclick='saveDDosModalChanges(this);'>保存\n" +
        "                                                            </button>\n" +
        "                                                        </div>\n" +
        "                                                    </div>\n" +
        "                                                </div>\n" +
        "                                            </div> <!--/modal certificate-->\n" +
        "\n" +
        "                                        </td>\n" +
        "                                        <td><input type=\"text\" value=\"123.231.32.123\" class=\"input-sm\"></td>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <span>443</span>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_13_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>轮询</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">一致性哈希</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this)\">随机</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_10_percent\">\n" +
        "                                            <button class=\"btn btn-link\" data-toggle='modal'\n" +
        "                                                    data-target='#aclAccessControlModal_waf0'>配置\n" +
        "                                            </button>\n" +
        "\n" +
        "                                            <!-- Modal acl access control config -->\n" +
        "                                            <div class='modal fade' id='aclAccessControlModal_waf0' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "                                                <div class='modal-dialog' role='document'  style=\"width: 1200px !important;\">\n" +
        "                                                    <div class='modal-content'>\n" +
        "                                                        <div class=\"modal-header\">\n" +
        "                                                            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span\n" +
        "                                                                    aria-hidden=\"true\">&times;</span></button>\n" +
        "                                                            <h4 class=\"modal-title\">ACL访问控制规则配置</h4>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-body'>\n" +
        "                                                            <div class=\"config-wrapper clearfix\" style=\"padding: 0px !important;\">\n" +
        "                                                                <table class=\"config-table table\" style=\"margin-bottom: 0 !important;\">\n" +
        "                                                                    <tbody>\n" +
        "\n" +
        "                                                                    <tr class=\"config-part\">\n" +
        "                                                                        <th><span>访问规则控制</span></th>\n" +
        "                                                                        <td>\n" +
        "                                                                            <div class=\"one-config  header-line\">\n" +
        "                                                                                <label class=\"config-name\">\n" +
        "                                                                                    <span>目标域名:www.ruiduncloud.com</span>\n" +
        "                                                                                </label>\n" +
        "\n" +
        "                                                                            </div>\n" +
        "\n" +
        "\n" +
        "                                                                            <div class=\"area-config\">\n" +
        "                                                                                <table class=\"table table-striped  protocol_td tbl_font_size\" id=\"tbl_domain_acl\">\n" +
        "                                                                                    <thead class=\"thead_pad\">\n" +
        "                                                                                    <tr>\n" +
        "                                                                                        <th>状态</th>\n" +
        "                                                                                        <th>规则名称</th>\n" +
        "                                                                                        <th>规则条件</th>\n" +
        "                                                                                        <th>动作</th>\n" +
        "                                                                                        <th>改变规则顺序</th>\n" +
        "                                                                                        <th>操作</th>\n" +
        "\n" +
        "                                                                                    </tr>\n" +
        "                                                                                    </thead>\n" +
        "                                                                                    <tbody>\n" +
        "\n" +
        "                                                                                    <tr>\n" +
        "                                                                                        <td class=\"td_5_percent\"><label class=\"label label-default\">未配置</label></td>\n" +
        "\n" +
        "                                                                                        <td class=\"td_20_percent\">\n" +
        "                                                                                            <input type=\"text\" class=\"input-sm\" placeholder=\"输入规则,例如user-agent\">\n" +
        "                                                                                        </td>\n" +
        "\n" +
        "                                                                                        <td class=\"td_20_percent\"><input type=\"text\" class=\"input-sm\"></td>\n" +
        "\n" +
        "                                                                                        <td class=\"td_20_percent\">\n" +
        "                                                                                            <div class=\"dropdown\">\n" +
        "                                                                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                                                                        class=\"btn btn-link \"\n" +
        "                                                                                                        aria-haspopup=\"true\"\n" +
        "                                                                                                        aria-expanded=\"false\">\n" +
        "                                                                                                    <span>阻断</span>\n" +
        "                                                                                                    <span class=\"caret\"></span>\n" +
        "                                                                                                </button>\n" +
        "                                                                                                <ul class=\"dropdown-menu\">\n" +
        "                                                                                                    <li onclick=\"selectProtoFwd(this);\">阻断</li>\n" +
        "                                                                                                    <li onclick=\"selectProtoFwd(this)\">放行</li>\n" +
        "                                                                                                </ul>\n" +
        "                                                                                            </div>\n" +
        "                                                                                        </td>\n" +
        "\n" +
        "                                                                                        <td class=\"td_15_percent\">\n" +
        "                                                                                            <button class=\"btn btn-link padding_zero\" onclick=\"moveCurTrPosition(this, 0);\">\n" +
        "\n" +
        "                                                                                                <li class=\"fa fa-arrow-circle-o-up\"></li>\n" +
        "                                                                                                上移\n" +
        "                                                                                            </button>\n" +
        "                                                                                            <label>|</label>\n" +
        "                                                                                            <button class=\"btn btn-link padding_zero\" onclick=\"moveCurTrPosition(this, 1);\">\n" +
        "                                                                                                <li class=\"fa fa-arrow-circle-o-down\"></li>\n" +
        "                                                                                                下移\n" +
        "                                                                                            </button>\n" +
        "                                                                                        </td>\n" +
        "                                                                                        <td class=\"td_20_percent\">\n" +
        "                                                                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                                                                确定\n" +
        "                                                                                            </button>\n" +
        "                                                                                            <label>|</label>\n" +
        "                                                                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                                                                    onclick=\"deleteCurRow(this,'','',4);\">\n" +
        "                                                                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                                                                删除\n" +
        "                                                                                            </button>\n" +
        "                                                                                        </td>\n" +
        "\n" +
        "                                                                                    </tr>\n" +
        "\n" +
        "\n" +
        "                                                                                    </tbody>\n" +
        "                                                                                </table>\n" +
        "                                                                                <div class=\"add_div_border\">\n" +
        "                                                                                    <button class=\"btn btn-link btn-sm\" onclick=\"btn_domain_acl_add(this, 3);\"\n" +
        "                                                                                            id=\"btn_domain_acl_add\">\n" +
        "                                                                                        <img width=\"20px\" height=\"20px\" src=\"images/add.png\">\n" +
        "                                                                                        <em>添加</em>\n" +
        "                                                                                    </button>\n" +
        "                                    <span id=\"span_domain_acl_num\">\n" +
        "                                        您还可以添加<Strong id=\"avail_domain_acl_num\">9</Strong>个域名\n" +
        "                                    </span>\n" +
        "                                                                                </div>\n" +
        "                                                                            </div>\n" +
        "                                                                        </td>\n" +
        "                                                                    </tr>\n" +
        "                                                                    <tbody>\n" +
        "                                                                </table>\n" +
        "                                                            </div>\n" +
        "                                                        </div>\n" +
        "                                                        <div class='modal-footer'>\n" +
        "                                                            <button id='aclAccessControlSave' type='button' class='btn btn-primary'\n" +
        "                                                                    onclick='saveDDosModalChanges(this);'>保存\n" +
        "                                                            </button>\n" +
        "                                                            <button id='aclAccessControlCancel' type='button' class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                                                            </button>\n" +
        "                                                        </div>\n" +
        "                                                    </div>\n" +
        "                                                </div>\n" +
        "                                            </div> <!--/acl modal-->\n" +
        "\n" +
        "\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <div>\n" +
        "                                                <input type=\"checkbox\" checked data-toggle=\"toggle\" data-size=\"mini\"/>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_waf_defend','avail_waf_defend_num',2);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "                                    </tr>\n" +
        "\n" +
        "\n" +
        "                                    </tbody>\n" +
        "                                </table>\n" +
        "                                <div class=\"add_div_border\">\n" +
        "                                    <button class=\"btn btn-link btn-sm\" onclick=\"btn_waf_add();\"\n" +
        "                                            id=\"btn_waf_defend_add\">\n" +
        "                                        <img width=\"20px\" height=\"20px\" src=\"images/add.png\">\n" +
        "                                        <em>添加</em>\n" +
        "                                    </button>\n" +
        "                                    <span id=\"span_waf_defend_num\">\n" +
        "                                        您还可以添加<Strong id=\"avail_waf_defend_num\">9</Strong>个域名\n" +
        "                                    </span>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "                        </td>\n";
    ;
    return str;
}
function getBlackWhiteListModal(modal_id, tag) {
    var tmpId = getPrefix(tag);

    var str = "<div class='modal fade' id='blackWhiteListModal" + tmpId + modal_id + "' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "    <div class='modal-dialog' role='document'>\n" +
        "        <div class='modal-content'>\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" onclick='closeDDosModals(this, 1);' aria-label=\"Close\"><span\n" +
        "                        aria-hidden=\"true\">&times;</span></button>\n" +
        "                <h4 class=\"modal-title\" id=\"myModalLabel\">添加黑白名单</h4>\n" +
        "            </div>\n" +
        "            <div class='modal-body'>\n" +
        "                <div class='pull-left'>\n" +
        "                    <h4><span class=\"modal-tab-color\">|</span>&nbsp;&nbsp;IP黑名单</h4>\n" +
        "                </div>\n" +
        "                <textarea class='modal-textarea'></textarea>\n" +
        "<div style='color:#F00'></div>" +
        "\n" +
        "                <div class='pull-left'>\n" +
        "                    <h4><span class=\"modal-tab-color\">|</span>&nbsp;&nbsp;IP白名单</h4>\n" +
        "                </div>\n" +
        "                <textarea class='modal-textarea'></textarea>\n" +
        "<div style='color:#F00'></div>" +
        "\n" +
        "                <div class='black-white-list-alert'>\n" +
        "                    <p>使用回车/换行分隔多个IP，支持网段添加如127.0.0.1/24，最多100个</p>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "            <div class='modal-footer'>\n" +
        "                <button id='blackWhiteListCancel' type='button' class='btn btn-default' onclick='closeDDosModals(this, 1);'>关闭\n" +
        "                </button>\n" +
        "                <button id='blackWhiteListConfirm' type='button' class='btn btn-primary' onclick='saveDDosModalChanges(this, 1);'>保存</button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>";

    return str;
}

function getAclAccessControlModal(modal_id, tag) {
    var tmpId = getPrefix(tag);

    var str = "<div class='modal fade' id='aclAccessControlModal" + tmpId + modal_id + "' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "    <div class='modal-dialog' role='document'  style=\"width: 1200px !important;\">\n" +
        "        <div class='modal-content'>\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span\n" +
        "                        aria-hidden=\"true\">&times;</span></button>\n" +
        "                <h4 class=\"modal-title\">ACL访问控制规则配置</h4>\n" +
        "            </div>\n" +
        "            <div class='modal-body'>\n" +
        "                <div class=\"config-wrapper clearfix\" style=\"padding: 0px !important;\">\n" +
        "                    <table class=\"config-table table\" style=\"margin-bottom: 0 !important;\">\n" +
        "                        <tbody>\n" +
        "\n" +
        "                        <tr class=\"config-part\">\n" +
        "                            <th><span>访问规则控制</span></th>\n" +
        "                            <td>\n" +
        "                                <div class=\"one-config  header-line\">\n" +
        "                                    <label class=\"config-name\">\n" +
        "                                        <span>目标域名:www.ruiduncloud.com</span>\n" +
        "                                    </label>\n" +
        "\n" +
        "                                </div>\n" +
        "\n" +
        "\n" +
        "                                <div class=\"area-config\">\n" +
        "                                    <table class=\"table table-striped  protocol_td tbl_font_size\" id=\"tbl_domain_acl" + tmpId + modal_id + "\">\n" +
        "                                        <thead class=\"thead_pad\">\n" +
        "                                        <tr>\n" +
        "                                            <th>状态</th>\n" +
        "                                            <th>规则名称</th>\n" +
        "                                            <th>规则条件</th>\n" +
        "                                            <th>动作</th>\n" +
        "                                            <th>改变规则顺序</th>\n" +
        "                                            <th>操作</th>\n" +
        "\n" +
        "                                        </tr>\n" +
        "                                        </thead>\n" +
        "                                        <tbody>\n" +
        "\n" +
        "                                        <tr>\n" +
        "                                            <td class=\"td_5_percent\"><label class=\"label label-default\">未配置</label></td>\n" +
        "\n" +
        "                                            <td class=\"td_20_percent\">\n" +
        "                                                <input type=\"text\" class=\"input-sm\" placeholder=\"输入规则,例如user-agent\">\n" +
        "                                            </td>\n" +
        "\n" +
        "                                            <td class=\"td_20_percent\"><input type=\"text\" class=\"input-sm\"></td>\n" +
        "\n" +
        "                                            <td class=\"td_20_percent\">\n" +
        "                                                <div class=\"dropdown\">\n" +
        "                                                    <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                            class=\"btn btn-link \"\n" +
        "                                                            aria-haspopup=\"true\"\n" +
        "                                                            aria-expanded=\"false\">\n" +
        "                                                        <span>阻断</span>\n" +
        "                                                        <span class=\"caret\"></span>\n" +
        "                                                    </button>\n" +
        "                                                    <ul class=\"dropdown-menu\">\n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">阻断</li>\n" +
        "                                                        <li onclick=\"selectProtoFwd(this)\">放行</li>\n" +
        "                                                    </ul>\n" +
        "                                                </div>\n" +
        "                                            </td>\n" +
        "\n" +
        "                                            <td class=\"td_15_percent\">\n" +
        "                                                <button class=\"btn btn-link padding_zero\" onclick=\"moveCurTrPosition(this, 0);\">\n" +
        "\n" +
        "                                                    <li class=\"fa fa-arrow-circle-o-up\"></li>\n" +
        "                                                    上移\n" +
        "                                                </button>\n" +
        "                                                <label>|</label>\n" +
        "                                                <button class=\"btn btn-link padding_zero\" onclick=\"moveCurTrPosition(this, 1);\">\n" +
        "                                                    <li class=\"fa fa-arrow-circle-o-down\"></li>\n" +
        "                                                    下移\n" +
        "                                                </button>\n" +
        "                                            </td>\n" +
        "                                            <td class=\"td_20_percent\">\n" +
        "                                                <button class=\"btn btn-link padding_zero\"\n" +
        "                                                        onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                    <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                    确定\n" +
        "                                                </button>\n" +
        "                                                <label>|</label>\n" +
        "                                                <button class=\"btn btn-link padding_zero\"\n" +
        "                                                        onclick=\"deleteCurRow(this,'','',4);\">\n" +
        "                                                    <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                    删除\n" +
        "                                                </button>\n" +
        "                                            </td>\n" +
        "\n" +
        "                                        </tr>\n" +
        "\n" +
        "\n" +
        "                                        </tbody>\n" +
        "                                    </table>\n" +
        "                                    <div class=\"add_div_border\">\n" +
        "                                        <button class=\"btn btn-link btn-sm\" onclick=\"btn_domain_acl_add(this, 3);\"\n" +
        "                                                id=\"btn_domain_acl_add" + tmpId + modal_id + "\">\n" +
        "                                            <img width=\"20px\" height=\"20px\" src=\"images/add.png\">\n" +
        "                                            <em>添加</em>\n" +
        "                                        </button>\n" +
        "                                    <span id=\"span_domain_acl_num" + tmpId + modal_id + "\">\n" +
        "                                        您还可以添加<Strong id=\"avail_domain_acl_num" + tmpId + modal_id + "\">9</Strong>个域名\n" +
        "                                    </span>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "                            </td>\n" +
        "                        </tr>\n" +
        "                        <tbody>\n" +
        "                    </table>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "            <div class='modal-footer'>\n" +
        "                <button id='aclAccessControlSave' type='button' class='btn btn-primary'\n" +
        "                        onclick='saveDDosModalChanges(this);'>保存\n" +
        "                </button>\n" +
        "                <button id='aclAccessControlCancel' type='button' class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                </button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>";

    return str;
}

function btn_proto_add(obj) {
    var TOTAL = getTotal();//添加协议转发的总条数
    var tr_length = $("table[id$='tbl_proto_forward']>tbody").children("tr").length;
    var tr_str = "<tr>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_10_percent\">\n" +
        "<button type=\"button\" class=\"btn  btn-ddos-link\" disabled>"
        + getISPLink() +
        "</button>" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>TCP</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\" id=\"protocolslist\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">UDP</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">TCP</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <input type=\"text\" placeholder=\"端口\" class=\"input_port input-sm\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\"><input type=\"text\" placeholder=\"端口\"\n" +
        "                                                                        class=\"input_port input-sm\"></td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "<button class=\"btn btn-link \" data-toggle='modal' onclick='openDDosModals(this, 1); '>配置</button>\n"

        + getBlackWhiteListModal(tr_length, 1)
        +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>轮询</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\" id=\"loadbalances\">\n" +
        "<li onclick=\"selectProtoFwd(this);\">轮询</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">一致性哈希</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">随机</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\"><input type=\"text\" placeholder=\"逗号隔开，最多10个\"\n" +
        "                                                                         class=\"input-sm\"></td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div>\n" +
        "                                                <input type=\"checkbox\" checked data-toggle=\"toggle\"\n" +
        "                                                       data-size=\"mini\"/>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,1);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_proto_forward','avail_proto_forward_num',1);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "\n" +
        "                                        </td>\n" +
        "                                    </tr>";

    if (0 == tr_length) {
        $('#tbl_proto_forward').append(tr_str);
    } else {
        $('#tbl_proto_forward>tbody').append(tr_str);
    }

    $('input[data-size=mini]').bootstrapToggle();
    var leave = TOTAL - tr_length - 1;
    if (leave == 0) {
        $('#span_avail_proto_forward_num').text("协议转发规则已添满！");
        $('#btn_proto_forward').addClass("disabled");
    } else {
        $('#avail_proto_forward_num').text(leave);
    }

}
function btn_website_defend_add(obj) {
    var TOTAL = getTotal();
    var tr_length = $("table[id$='tbl_website_defend']>tbody").children("tr").length;
    var tr_str = "                                    <tr>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_10_percent\">\n" +
        "<button type=\"button\" class=\"btn  btn-ddos-link\" disabled>"
        + getISPLink() +
        "</button>" +
        "                                        </td>\n" +
        "                                        <td class=\"td_13_percent\">\n" +
        "                                            <input type=\"text\" class=\"input-sm\" placeholder=\"输入域名\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_10_percent\">\n" +
        "                                            <div class=\"checkbox margin_zero\">\n" +
        "                                                <label class=\"protocol_margin_left\">\n" +
        "                                                    <input type=\"radio\" name=\"protoRadios" + tr_length + "\"\n" +
        "                                                           onclick=\"protoRadiosClick(this, '', 2);\" value=\"http\" checked> HTTP\n" +
        "                                                </label>\n" +
        "                                            </div>\n" +
        "                                            <div class=\"checkbox margin_zero\">\n" +
        "                                                <label class=\"protocol_margin_left\">\n" +
        "                                                    <input type=\"radio\" name=\"protoRadios" + tr_length + "\"\n" +
        "                                                           onclick=\"protoRadiosClick(this," + tr_length + ",2);\" value=\"https\"\n" +
        "                                                            > HTTPS\n" +
        "                                                </label>\n" +
        "                                            </div>\n" +
        getUploadCertificateModal(tr_length, 2) +
        "                                        </td>\n" +
        "                                        <td class=\"td_13_percent\"><input type=\"text\" value=\"123.231.32.123\" class=\"input-sm\"></td>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <span>443</span>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>轮询</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\">\n" +
        "<li onclick=\"selectProtoFwd(this);\">轮询</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">一致性哈希</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this)\">随机</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "<button class=\"btn btn-link\"  data-toggle='modal' onclick='openDDosModals(this, 1); '>配置</button>\n"
        + "" + getBlackWhiteListModal(tr_length, 2) +


        "\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "                                            <div>\n" +
        "                                                <input type=\"checkbox\" checked data-toggle=\"toggle\" data-size=\"mini\"/>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_website_defend','avail_website_defend_num',2);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "                                    </tr>\n";


    $('#tbl_website_defend>tbody').append(tr_str);
    $('input[data-size=mini]').bootstrapToggle();


    var leave = TOTAL - tr_length - 1;
    if (leave == 0) {
        $('#span_website_defend_num').text("网站防护已添满！");
        $('#btn_website_defend_add').addClass("disabled");
    } else {
        $('#avail_website_defend_num').text(leave);
    }
}
function btn_rule_add() {
    var TOTAL = getTotalRulesNum();//添加协议转发的总条数
    var tr_length = $("table[id$='tbl_rules_config']>tbody").children("tr").length;
    var rowStr = "<tr>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_13_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>后缀名</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">后缀名</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this)\">目录</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <input type=\"text\" class=\"input-sm\" >\n" +
        "                                        </td>\n" +
        "\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "\n" +
        "                                            <div class=\"input-group\" style=\"width: 175px;\">\n" +
        "                                                <input type=\"text\" class=\"form-control\"\n" +
        "                                                       style=\"width: 60px;float: right;\">\n" +
        "\n" +
        "                                                <div class=\"input-group-btn\">\n" +
        "                                                    <button type=\"button\" class=\"btn btn-default dropdown-toggle\"\n" +
        "                                                            data-toggle=\"dropdown\" aria-haspopup=\"true\"\n" +
        "                                                            aria-expanded=\"false\">\n" +
        "                                                        <span>小时</span>\n" +
        "                                                        <span class=\"caret\"></span>\n" +
        "                                                    </button>\n" +
        "                                                    <ul class=\"dropdown-menu dropdown-menu-right\">\n" +
        "                                                        \n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">分钟</li>\n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">小时</li>\n" +
        "                                                        <li onclick=\"selectProtoFwd(this);\">&nbsp;&nbsp;&nbsp;天</li>\n" +
        "                                                    </ul>\n" +
        "                                                </div>\n" +
        "                                                <!-- /btn-group -->\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <input type=\"text\" placeholder=\"权重\"\n" +
        "                                                   class=\"input-sm\" style=\"width: 50px !important;\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_rules_config','avail_rules_num',3);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "\n" +
        "                                    </tr>";

    if (0 == tr_length) {
        $('#tbl_rules_config').append(rowStr);
    } else {
        $('#tbl_rules_config>tbody').append(rowStr);
    }

    $('input[data-size=mini]').bootstrapToggle();
    var leave = TOTAL - tr_length - 1;
    if (leave == 0) {
        $('#span_rules_num').text("配置规则已添满！");
        $('#btn_rules_add').addClass("disabled");
    } else {
        $('#avail_rules_num').text(leave);
    }
}
function btn_waf_add() {
    var TOTAL = getTotal();//添加协议转发的总条数
    var tr_length = $("table[id$='tbl_waf_defend']>tbody").children("tr").length;
    var rowStr =


        "<tr>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <label class=\"label label-default\">未配置</label>\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <input type=\"text\" class=\"input-sm\" placeholder=\"输入域名\">\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_8_percent\">\n" +
        "\n" +
        "\n" +
        "                                            <div class=\"checkbox margin_zero\">\n" +
        "                                                <label>\n" +
        "                                                    <input type=\"radio\" name=\"protoRadios\"\n" +
        "                                                           onclick=\"protoRadiosClick(this);\" value=\"http\"> HTTP&nbsp;&nbsp;\n" +
        "                                                </label>\n" +
        "                                            </div>\n" +
        "                                            <div class=\"checkbox margin_zero\">\n" +
        "                                                <label>\n" +
        "                                                    <input type=\"radio\" name=\"protoRadios\"\n" +
        "                                                           onclick=\"protoRadiosClick(this," + tr_length + ",3);\" value=\"https\"\n" +
        "                                                            > HTTPS\n" +
        "                                                </label>\n" +
        getUploadCertificateModal(tr_length, 3) +
        "                                            </div>\n" +
        "\n" +
        "                                          \n" +
        "\n" +
        "                                        </td>\n" +
        "                                        <td><input type=\"text\" value=\"123.231.32.123\" class=\"input-sm\"></td>\n" +
        "                                        <td class=\"td_5_percent\">\n" +
        "                                            <span>443</span>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_13_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>轮询</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">一致性哈希</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this)\">随机</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_10_percent\">\n" +
        "                                            <button class=\"btn btn-link\" data-toggle='modal'\n" +
        "                                                    data-target='#aclAccessControlModal" + getPrefix(3) + tr_length + "'>配置\n" +
        "                                            </button>\n" +
        "\n" + getAclAccessControlModal(tr_length, 3) +
        "                                          \n" +
        "\n" +
        "                                        </td>\n" +
        "                                        <td>\n" +
        "                                            <div>\n" +
        "                                                <input type=\"checkbox\" checked data-toggle=\"toggle\" data-size=\"mini\"/>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_waf_defend','avail_waf_defend_num',2);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "                                    </tr>";


    if (0 == tr_length) {
        $('#tbl_waf_defend').append(rowStr);
    } else {
        $('#tbl_waf_defend>tbody').append(rowStr);
    }

    $('input[data-size=mini]').bootstrapToggle();
    var leave = TOTAL - tr_length - 1;
    if (leave == 0) {
        $('#span_waf_defend_num').text("配置规则已添满！");
        $('#btn_waf_defend_add').addClass("disabled");
    } else {
        $('#avail_waf_defend_num').text(leave);
    }
}
function btn_domain_acl_add(obj, tag) {
    var tepId = getPrefix(tag);
    var TOTAL = getTotalAclNum();//添加协议转发的总条数
    var table = $(obj).parent().prev();
    var tr_length = $(table).find("tbody").children("tr").length;
    var rowStr = "<tr>\n" +
        "                                        <td class=\"td_5_percent\"><label class=\"label label-default\">未配置</label></td>\n" +
        "\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <input type=\"text\" class=\"input-sm\" placeholder=\"输入规则,例如user-agent\">\n" +
        "                                        </td>\n" +
        "\n" +
        "                                        <td class=\"td_20_percent\"><input type=\"text\" class=\"input-sm\"></td>\n" +
        "\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <div class=\"dropdown\">\n" +
        "                                                <button type=\"button\" data-toggle=\"dropdown\"\n" +
        "                                                        class=\"btn btn-link \"\n" +
        "                                                        aria-haspopup=\"true\"\n" +
        "                                                        aria-expanded=\"false\">\n" +
        "                                                    <span>阻断</span>\n" +
        "                                                    <span class=\"caret\"></span>\n" +
        "                                                </button>\n" +
        "                                                <ul class=\"dropdown-menu\">\n" +
        "                                                    <li onclick=\"selectProtoFwd(this);\">阻断</li>\n" +
        "                                                    <li onclick=\"selectProtoFwd(this)\">放行</li>\n" +
        "                                                </ul>\n" +
        "                                            </div>\n" +
        "                                        </td>\n" +
        "\n" +
        "                                        <td class=\"td_15_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\" onclick=\"moveCurTrPosition(this, 0);\">\n" +
        "\n" +
        "                                                <li class=\"fa fa-arrow-circle-o-up\"></li>\n" +
        "                                                上移\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\" onclick=\"moveCurTrPosition(this, 1);\">\n" +
        "                                                <li class=\"fa fa-arrow-circle-o-down\"></li>\n" +
        "                                                下移\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "                                        <td class=\"td_20_percent\">\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"confirmUpdate(this,2);\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link padding_zero\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'','',4);\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                        </td>\n" +
        "\n" +
        "                                    </tr>";

    $(table).find("tbody").append(rowStr);

    $('input[data-size=mini]').bootstrapToggle();
    var leave = TOTAL - tr_length - 1;
    if (leave == 0) {
        $(obj).next().text("域名已满！");
        $(obj).addClass("disabled");
    } else {
        $(obj).next().children("strong").text(leave);
    }
}

function getCdnModal() {
    var str = "<div class='modal fade' id='filterParaConfigModal' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "    <div class='modal-dialog' role='document'>\n" +
        "        <div class='modal-content'>\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span\n" +
        "                        aria-hidden=\"true\">&times;</span></button>\n" +
        "                <h4 class=\"modal-title\">过滤参数设置</h4>\n" +
        "            </div>\n" +
        "            <div class='modal-body'>\n" +
        "                <div class=\"row certificate-row\">\n" +
        "                    <div class=\"col-md-3\"><p class=\"modal-left-text\">设置保留参数:</p></div>\n" +
        "                    <div class=\"col-md-9\">\n" +
        "                        <div class=\"form-group\">\n" +
        "                            <label class=\"sr-only\">保留参数</label>\n" +
        "                            <input type=\"text\" class=\"form-control\" id=\"filterRetainParaInput\">\n" +
        "                        </div>\n" +
        "                        <p class=\"modal-input-text-hint\">多个参数请使用西文逗号隔开，总数不超过10个</p>\n" +
        "                    </div>\n" +
        "                </div>\n" +
        "\n" +
        "            </div>\n" +
        "            <div class='modal-footer'>\n" +
        "                <button id='filterParaConfigConfirm' type='button' class='btn btn-primary'\n" +
        "                        onclick='saveDDosModalChanges(this);'>保存\n" +
        "                </button>\n" +
        "                <button id='filterParaConfigCancel' type='button' class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                </button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>\n" +
        "<!-- Modal loop host config -->\n" +
        "<div class='modal fade' id='loopSourceHostConfigModal' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "    <div class='modal-dialog' role='document'>\n" +
        "        <div class='modal-content'>\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span\n" +
        "                        aria-hidden=\"true\">&times;</span></button>\n" +
        "                <h4 class=\"modal-title\">过滤参数设置</h4>\n" +
        "            </div>\n" +
        "            <div class='modal-body'>\n" +
        "                <div class=\"row certificate-row\">\n" +
        "                    <div class=\"col-md-2\"><p class=\"modal-left-text\">类型:</p></div>\n" +
        "                    <div class=\"col-md-9\">\n" +
        "                        <div class=\"form-group\">\n" +
        "                            <label class=\"sr-only\">域名类型</label>\n" +
        "\n" +
        "                            <div class=\"btn-group\" role=\"group\">\n" +
        "                                <button type=\"button\" class=\"btn btn-default dropdown-toggle\" data-toggle=\"dropdown\"\n" +
        "                                        aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                    <span id=\"checkHostTypeDropdown\">自定义域名</span>\n" +
        "                                    <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>\n" +
        "                                    <span class=\"caret\"></span>\n" +
        "                                </button>\n" +
        "                                <ul class=\"dropdown-menu\" id=\"checkHostTypeul\">\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">自定义域名</a></li>\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">标准域名</a></li>\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">其他域名</a></li>\n" +
        "                                </ul>\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "                        <div class=\"form-group\">\n" +
        "                            <label class=\"sr-only\">请输入域名</label>\n" +
        "                            <input type=\"text\" class=\"form-control\" id=\"inputLoopSourceHost\">\n" +
        "                        </div>\n" +
        "                        <p class=\"modal-input-text-hint\">请输入正确的域名</p>\n" +
        "                    </div>\n" +
        "                </div>\n" +
        "\n" +
        "            </div>\n" +
        "            <div class='modal-footer'>\n" +
        "                <button id='loopHostConfigConfirm' type='button' class='btn btn-primary'\n" +
        "                        onclick='saveDDosModalChanges(this);'>保存\n" +
        "                </button>\n" +
        "                <button id='loopHostConfigCancel' type='button' class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                </button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>\n" +
        "<div class='modal fade' id='custom404PageConfig1Modal' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "    <div class='modal-dialog' role='document'>\n" +
        "        <div class='modal-content'>\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span\n" +
        "                        aria-hidden=\"true\">&times;</span></button>\n" +
        "                <h4 class=\"modal-title\">自定义404页面</h4>\n" +
        "            </div>\n" +
        "            <div class='modal-body'>\n" +
        "                <div class=\"row certificate-row\">\n" +
        "                    <div class=\"col-md-2\"><p class=\"modal-left-text\">类型:</p></div>\n" +
        "                    <div class=\"col-md-9\">\n" +
        "                        <div class=\"form-group\">\n" +
        "                            <label class=\"sr-only\">404类型</label>\n" +
        "\n" +
        "                            <div class=\"btn-group\" role=\"group\">\n" +
        "                                <button type=\"button\" class=\"btn btn-default dropdown-toggle\" data-toggle=\"dropdown\"\n" +
        "                                        aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                    <span id=\"custom404pageType1Dropdown\">自定义404</span>\n" +
        "                                    <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>\n" +
        "                                    <span class=\"caret\"></span>\n" +
        "                                </button>\n" +
        "                                <ul class=\"dropdown-menu\" id=\"custom404pageType1ul\">\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">自定义404</a></li>\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">公益404</a></li>\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">默认404</a></li>\n" +
        "                                </ul>\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "                        <div class=\"form-group\">\n" +
        "                            <label class=\"sr-only\">请输入域名</label>\n" +
        "                            <input type=\"text\" class=\"form-control\" id=\"custom404pageURL\"\n" +
        "                                   placeholder=\"http://www.ruiduncloud.com/...\">\n" +
        "                        </div>\n" +
        "                        <p class=\"modal-input-text-hint\">请输入自定义的404页面的链接URL例如：\n" +
        "                            http://www.ruiduncloud.com/error.html注意：该文件资源需要存储在源站，使用加速域名\n" +
        "                        </p>\n" +
        "                    </div>\n" +
        "                </div>\n" +
        "\n" +
        "            </div>\n" +
        "            <div class='modal-footer'>\n" +
        "                <button id='custom404PageConfig1Confirm' type='button' class='btn btn-primary'\n" +
        "                        onclick='saveDDosModalChanges(this);'>保存\n" +
        "                </button>\n" +
        "                <button id='custom404PageConfig1Cancel' type='button' class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                </button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>\n" +
        "<!-- Modal custom 404 page2 -->\n" +
        "<div class='modal fade' id='custom404PageConfig2Modal' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "    <div class='modal-dialog' role='document'>\n" +
        "        <div class='modal-content'>\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span\n" +
        "                        aria-hidden=\"true\">&times;</span></button>\n" +
        "                <h4 class=\"modal-title\">自定义404页面</h4>\n" +
        "            </div>\n" +
        "            <div class='modal-body'>\n" +
        "                <div class=\"row certificate-row\">\n" +
        "                    <div class=\"col-md-2\"><p class=\"modal-left-text\">类型:</p></div>\n" +
        "                    <div class=\"col-md-9\">\n" +
        "                        <div class=\"form-group\">\n" +
        "                            <label class=\"sr-only\">404类型</label>\n" +
        "\n" +
        "                            <div class=\"btn-group\" role=\"group\">\n" +
        "                                <button type=\"button\" class=\"btn btn-default dropdown-toggle\" data-toggle=\"dropdown\"\n" +
        "                                        aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                    <span id=\"custom404pageType2Dropdown\">公益404</span>\n" +
        "                                    <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>\n" +
        "                                    <span class=\"caret\"></span>\n" +
        "                                </button>\n" +
        "                                <ul class=\"dropdown-menu\" id=\"custom404pageType2ul\">\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">公益404</a></li>\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">自定义404</a></li>\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">默认404</a></li>\n" +
        "                                </ul>\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "                        <p class=\"modal-input-text-hint\">http返回404时，跳转到包含有公益信息404页面，该页面完全公益，不会造成任何流量费用，查看详情\n" +
        "                        </p>\n" +
        "                    </div>\n" +
        "                </div>\n" +
        "\n" +
        "            </div>\n" +
        "            <div class='modal-footer'>\n" +
        "                <button id='custom404PageConfig2Confirm' type='button' class='btn btn-primary'\n" +
        "                        onclick='saveDDosModalChanges(this);'>保存\n" +
        "                </button>\n" +
        "                <button id='custom404PageConfig2Cancel' type='button' class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                </button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>\n" +
        "<!-- Modal custom 404 page3 -->\n" +
        "<div class='modal fade' id='custom404PageConfig3Modal' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "    <div class='modal-dialog' role='document'>\n" +
        "        <div class='modal-content'>\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span\n" +
        "                        aria-hidden=\"true\">&times;</span></button>\n" +
        "                <h4 class=\"modal-title\">自定义404页面</h4>\n" +
        "            </div>\n" +
        "            <div class='modal-body'>\n" +
        "                <div class=\"row certificate-row\">\n" +
        "                    <div class=\"col-md-2\"><p class=\"modal-left-text\">类型:</p></div>\n" +
        "                    <div class=\"col-md-9\">\n" +
        "                        <div class=\"form-group\">\n" +
        "                            <label class=\"sr-only\">404类型</label>\n" +
        "\n" +
        "                            <div class=\"btn-group\" role=\"group\">\n" +
        "                                <button type=\"button\" class=\"btn btn-default dropdown-toggle\" data-toggle=\"dropdown\"\n" +
        "                                        aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                    <span id=\"custom404pageType3Dropdown\">公益404</span>\n" +
        "                                    <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>\n" +
        "                                    <span class=\"caret\"></span>\n" +
        "                                </button>\n" +
        "                                <ul class=\"dropdown-menu\" id=\"custom404pageType3ul\">\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">默认404</a></li>\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">公益404</a></li>\n" +
        "                                    <li onclick=\"selectWafAccessControlMatch(this)\"><a href=\"#\">自定义404</a></li>\n" +
        "                                </ul>\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "                        <p class=\"modal-input-text-hint\">服务器默认404页面\n" +
        "                        </p>\n" +
        "                    </div>\n" +
        "                </div>\n" +
        "\n" +
        "            </div>\n" +
        "            <div class='modal-footer'>\n" +
        "                <button id='custom404PageConfig3Confirm' type='button' class='btn btn-primary'\n" +
        "                        onclick='saveDDosModalChanges(this);'>保存\n" +
        "                </button>\n" +
        "                <button id='custom404PageConfig3Cancel' type='button' class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                </button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>\n" +
        "<!-- Modal anti stealing link config -->\n" +
        "<div class='modal fade' id='antiStealingLinkModal' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "    <div class='modal-dialog' role='document'>\n" +
        "        <div class='modal-content'>\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span\n" +
        "                        aria-hidden=\"true\">&times;</span></button>\n" +
        "                <h4 class=\"modal-title\">防盗链配置</h4>\n" +
        "            </div>\n" +
        "            <div class='modal-body'>\n" +
        "                <div class='pull-left'>\n" +
        "                    <h5><span class=\"modal-tab-color\">|</span>&nbsp;&nbsp;Refer黑名单</h5>\n" +
        "                </div>\n" +
        "                <textarea class='modal-textarea' id=\"ReferBlackListTextArea\">www.a.com\n" +
        "                www.b.com</textarea>\n" +
        "\n" +
        "                <div class='pull-left'>\n" +
        "                    <h5><span class=\"modal-tab-color\">|</span>&nbsp;&nbsp;Refer白名单</h5>\n" +
        "                </div>\n" +
        "                <textarea class='modal-textarea' id=\"ReferWhiteListTextArea\">www.c.com</textarea>\n" +
        "\n" +
        "                <div class='black-white-list-alert'>\n" +
        "                    <p class=\"modal-input-text-hint\">使用回车/换行分隔多个域名，最多100个</p>\n" +
        "                </div>\n" +
        "\n" +
        "            </div>\n" +
        "            <div class='modal-footer'>\n" +
        "                <button id='antiStealingLinkConfirm' type='button' class='btn btn-primary'\n" +
        "                        onclick='saveDDosModalChanges(this);'>保存\n" +
        "                </button>\n" +
        "                <button id='antiStealingLinkCancel' type='button' class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                </button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>\n" +
        "<!-- Modal waf access control config -->\n" +
        "<div class='modal fade' id='wafAccessControlModal' tabindex=\"-1\" role='dialog' aria-labledby='#myModalLabel'>\n" +
        "    <div class='modal-dialog' role='document'>\n" +
        "        <div class='modal-content'>\n" +
        "            <div class=\"modal-header\">\n" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span\n" +
        "                        aria-hidden=\"true\">&times;</span></button>\n" +
        "                <h4 class=\"modal-title\">添加规则</h4>\n" +
        "            </div>\n" +
        "            <div class='modal-body'>\n" +
        "                <label for=\"wafAccessControlRuleName\">规则名称：&nbsp;&nbsp;</label>\n" +
        "                <input type=\"text\" class=\"form-control\" id=\"wafAccessControlRuleName\">\n" +
        "\n" +
        "                <div class=\"form-group\">\n" +
        "                    <label for=\"wafAccessControlRuleTable\" class=\"wafRuleMatchLabel\">匹配条件:</label>\n" +
        "                    <table class=\"table table-striped waf-rule_table\" id=\"wafAccessControlRuleTable\">\n" +
        "                        <thead>\n" +
        "                        <tr>\n" +
        "                            <th>匹配字段</th>\n" +
        "                            <th>逻辑符</th>\n" +
        "                            <th>匹配内容</th>\n" +
        "                        </tr>\n" +
        "                        </thead>\n" +
        "                        <!--/thead-->\n" +
        "                        <tbody>\n" +
        "                        <tr>\n" +
        "                            <td>\n" +
        "                                <div class=\"btn-group\" role=\"group\">\n" +
        "                                    <button type=\"button\" class=\"btn btn-default dropdown-toggle form-control\"\n" +
        "                                            data-toggle=\"dropdown\"\n" +
        "                                            aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                        <span>URL</span>\n" +
        "                                        <span class=\"caret\"></span>\n" +
        "                                    </button>\n" +
        "                                    <ul class=\"dropdown-menu\" id=\"wafAccessControlRuleMatchURLType\">\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">URL</a></li>\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">域名</a></li>\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">端口号</a></li>\n" +
        "                                    </ul>\n" +
        "                                </div>\n" +
        "                            </td>\n" +
        "                            <td>\n" +
        "                                <div class=\"btn-group\" role=\"group\">\n" +
        "                                    <button type=\"button\" class=\"btn btn-default dropdown-toggle form-control\"\n" +
        "                                            data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                        <span>包含</span>\n" +
        "                                        <span class=\"caret\"></span>\n" +
        "                                    </button>\n" +
        "                                    <ul class=\"dropdown-menu\" id=\"wafAccessControlRuleLogicSymbol1Type\">\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">包含</a></li>\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">不包含</a></li>\n" +
        "                                    </ul>\n" +
        "                                </div>\n" +
        "                            </td>\n" +
        "                            <td>\n" +
        "                                <div role=\"alert\">\n" +
        "                                    <button type=\"button\" class=\"close close-tr\" onclick=\"deleteWafRule(this);\">\n" +
        "                                        <span aria-hidden=\"true\">&times;</span>\n" +
        "                                    </button>\n" +
        "                                    <input type=\"text\" class=\"form-control\" style=\"width: 90%\"\n" +
        "                                           placeholder=\"只允许填写一个匹配项，不填代表空\">\n" +
        "                                </div>\n" +
        "                            </td>\n" +
        "                        </tr>\n" +
        "                        <tr>\n" +
        "                            <td>\n" +
        "                                <div class=\"btn-group\" role=\"group\">\n" +
        "                                    <button type=\"button\" class=\"btn btn-default dropdown-toggle form-control\"\n" +
        "                                            data-toggle=\"dropdown\"\n" +
        "                                            aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                        <span>Refer</span>\n" +
        "                                        <span class=\"caret\"></span>\n" +
        "                                    </button>\n" +
        "                                    <ul class=\"dropdown-menu\" id=\"wafAccessControlRuleMatchReferType\">\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">URL</a></li>\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">域名</a></li>\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">端口号</a></li>\n" +
        "                                    </ul>\n" +
        "                                </div>\n" +
        "                            </td>\n" +
        "                            <td>\n" +
        "                                <div class=\"btn-group\" role=\"group\">\n" +
        "                                    <button type=\"button\" class=\"btn btn-default dropdown-toggle form-control\"\n" +
        "                                            data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                        <span>包含</span>\n" +
        "                                        <span class=\"caret\"></span>\n" +
        "                                    </button>\n" +
        "                                    <ul class=\"dropdown-menu\" id=\"wafAccessControlRuleLogicSymbol2Type\">\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">包含</a></li>\n" +
        "                                        <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">不包含</a></li>\n" +
        "                                    </ul>\n" +
        "                                </div>\n" +
        "                            </td>\n" +
        "                            <td>\n" +
        "                                <div role=\"alert\">\n" +
        "                                    <button type=\"button\" class=\"close close-tr\" onclick=\"deleteWafRule(this);\">\n" +
        "                                        <span aria-hidden=\"true\">&times;</span>\n" +
        "                                    </button>\n" +
        "                                    <input type=\"text\" class=\"form-control\" style=\"width: 90%\"\n" +
        "                                           placeholder=\"只允许填写一个匹配项，不填代表空\">\n" +
        "                                </div>\n" +
        "                            </td>\n" +
        "                        </tr>\n" +
        "                        </tbody>\n" +
        "                        <!--/tbody-->\n" +
        "                    </table>\n" +
        "                    <!--/table-->\n" +
        "                </div>\n" +
        "                <form class=\"form-inline\">\n" +
        "                    <div class=\"form-group\">\n" +
        "                        <label class=\"wafRuleMatchLabel\">匹配动作：</label>\n" +
        "\n" +
        "                        <div class=\"btn-group\" role=\"group\">\n" +
        "                            <button type=\"button\"\n" +
        "                                    class=\"btn btn-default dropdown-toggle form-control wafAccessControlRuleActionType\"\n" +
        "                                    data-toggle=\"dropdown\"\n" +
        "                                    aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
        "                                <span>放行</span>\n" +
        "                                <span class=\"caret\" style=\"margin: 0 0px 0 20px !important; position: relative\"></span>\n" +
        "                            </button>\n" +
        "                            <ul class=\"dropdown-menu\" id=\"wafAccessControlRuleActionType\">\n" +
        "                                <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">放行</a></li>\n" +
        "                                <li onclick=\"selectWafAccessControlMatch(this);\"><a href=\"#\">拦截</a></li>\n" +
        "                            </ul>\n" +
        "                        </div>\n" +
        "                    </div>\n" +
        "                </form>\n" +
        "            </div>\n" +
        "            <div class='modal-footer'>\n" +
        "                <button id='wafAccessControlConfirm' type='button' class='btn btn-primary'\n" +
        "                        onclick='saveDDosModalChanges(this);'>保存\n" +
        "                </button>\n" +
        "                <button id='wafAccessControlCancel' type='button' class='btn btn-default' data-dismiss='modal'>关闭\n" +
        "                </button>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "        <!--/modal-content-->\n" +
        "    </div>\n" +
        "    <!--/modal-dialog-->\n" +
        "</div>";
    return str;
}

function protoRadiosClick(obj, modal_id, tag) {
    var tr = $(obj).parent().parent().parent().parent();
    if ($(obj).val() == 'http') {
        if (tag == 3) {
            tr.find('td:eq(4)').text("80");
        }
        else if (tag == 2) {
            tr.find('td:eq(5)').text("80");
        }
        return;
    } else {
        if (tag == 3) {
            tr.find('td:eq(4)').text("443");
        }
        else if (tag == 2) {
            tr.find('td:eq(5)').text("443");
        }
    }
    var prefix = getPrefix(tag);
    //alert('#uploadCertificateModal' + prefix + modal_id);
    openDDosModals(obj, 2);
    //$('#uploadCertificateModal' + prefix + modal_id).modal('show');
}
function protoCheckBoxClick(obj, modal_id) {
    var tr = $(obj).parent().parent().parent().parent();

    if ($(obj).val() == 'http') {
        tr.find('td:eq(3)').children("img").attr("src", "images/before_config.png");
        return;
    } else if ($(obj).is(':checked')) {
        tr.find('td:eq(3)').children("img").attr("src", "images/after_config.png");
        $("#" + modal_id).modal("show");
    } else {
        tr.find('td:eq(3)').children("img").attr("src", "images/before_config.png");
    }
}


function updateCurRow(obj, tag) {

    var tr = $(obj).parent().parent();

    //备份修改之前的信息
    if (tag == 1) {
        var portValue = fillDDosPortValue(tr);
        backUpPortValue[portValue.id + ''] = portValue;
    }
    else if (tag == 2) {
        var domainValue = fillDDosDomainValue(tr);
        backUpDomainValue[domainValue.id + ''] = domainValue;
    }

    var l = tr.find('label:first');
    l.removeClass('label-success');
    l.addClass('label-danger');
    l.text("配置中")
    tr.find('input[type=text]').each(function () {
        $(this).removeAttr("readonly");
        $(this).css("border", "2px inset lightgrey");
    });
    tr.find('button').each(function () {
        $(this).removeClass("disabled");
    });
    tr.find('td input[type=checkbox]').each(function () {
        $(this).removeAttr("disabled");
    });
    tr.find('td input[type=radio]').each(function () {
        $(this).removeAttr("disabled");
    });
    tr.find('td:last').html(onUpdateStr(tag));
}

function cancelUpdate(obj, tag) {
    var tr = $(obj).parent().parent();

    var l = tr.find('label:first');
    l.removeClass('label-danger');
    l.addClass('label-success');
    l.text("已配置")

    tr.find('input[type=text]').each(function () {
        $(this).css("border", "none");
        $(this).attr("readonly", "readonly");
    });
    tr.find('button').each(function () {
        $(this).addClass("disabled");
    });
    tr.find('td input[type=checkbox]').each(function () {
        $(this).attr("disabled", "true");
    });

    tr.find('td input[type=radio]').each(function () {
        $(this).attr("disabled", "true");
    });

    tr.find('td:last').html(onCancelStr(tag));


    //填充原始的数据
    var key = tr.attr("id");
    if (tag == 1) {
        console.log("backUpPortValue-->" + JSON.stringify(backUpPortValue));
        if (backUpPortValue.hasOwnProperty(key)) {
            var portValue = backUpPortValue[key];
            initPortValueTr(tr, portValue);
        }
    }
    else if (tag == 2) {
        console.log("backUpDomainValue-->" + JSON.stringify(backUpDomainValue));
        if (backUpDomainValue.hasOwnProperty(key)) {
            var domainValue = backUpDomainValue[key];
            initDomainValueTr(tr, domainValue);
        }
    }
}

///ddos Port and Domain confirm
function confirmUpdate(obj, tag) {

    var tr = $(obj).parent().parent();

    if(verifyDDosDetail(tr, tag)) {
        console.log("ddosPageDetail verify success");
        if (tag == 1) {//port
            var ddosPortValue = fillDDosPortValue(tr);
            savePortValue(tr, tag, ddosPortValue);
        } else {//domain
            var ddosDomainValue = fillDDosDomainValue(tr);
            saveDomainValue(tr, tag, ddosDomainValue);
        }
    }
    else {
        //alert("请检查检验内容！");
        return;
    }
}
function confirmUpdateHelper(tr, tag) {
    var l = tr.find('label:first');
    l.removeClass('label-default');
    l.removeClass('label-danger');
    l.addClass('label-success');
    l.text("已配置")

    tr.find('input[type=text]').each(function () {
        var rowno = $(this).closest("tr").index();
        $(this).css("border", "none");
        $(this).attr("readonly", "readonly");
        if ((rowno % 2) == 0) {
            $(this).css("background-color", "#f9f9f9");
        } else {
            $(this).css("background-color", "#ffffff");
        }
    });
    tr.find('button').each(function () {
        $(this).addClass("disabled");
    });
    tr.find('td input[type=checkbox]').each(function () {
        $(this).attr("disabled", "true");
    });

    tr.find('td input[type=radio]').each(function () {
        $(this).attr("disabled", "true");
    });

    tr.find('td:last').html(onCancelStr(tag));
}
function onCancelStr(tag) {
    var str = "<button class=\"btn btn-link\" style=\"padding: 0 !important;\"\n" +
        "                                                    onclick=\"deleteCurRow(this,'tbl_proto_forward','avail_proto_forward_num'," + tag + ");\">\n" +
        "                                                <li class=\"fa fa-cut\">&nbsp;</li>\n" +
        "                                                删除\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link\" style=\"padding: 0 !important;\"\n" +
        "                                                    onclick=\"updateCurRow(this," + tag + ");\">\n" +
        "                                                <li class=\"fa fa-reply\">&nbsp;</li>\n" +
        "                                                修改\n" +
        "                                            </button>";

    return str;
}
function onUpdateStr(tag) {
    var str = "<button class=\"btn btn-link\" style=\"padding: 0 !important;\"\n" +
        "                                                    onclick=\"confirmUpdate(this," + tag + ");\">\n" +
        "                                                <li class=\"fa fa-save\">&nbsp;</li>\n" +
        "                                                确定\n" +
        "                                            </button>\n" +
        "                                            <label>|</label>\n" +
        "                                            <button class=\"btn btn-link\" style=\"padding: 0 !important;\"\n" +
        "                                                    onclick=\"cancelUpdate(this," + tag + ");\">\n" +
        "                                                <li class=\"fa fa-undo\">&nbsp;</li>\n" +
        "                                                取消\n" +
        "                                            </button>";
    return str;
}


/**
 *
 * @param obj
 * @param tbl_id
 * @param target_id
 * @param tag 1-协议转发 2-网站防护 3-waf规则 4-cdn域名
 */
function deleteCurRow(obj, tbl_id, target_id, tag) {
    if(!confirm("请确认是否删除？")) return;
    var trDel = $(obj).parent().parent();


    var url = "";
    if ($(trDel).attr("id") != null) {

        if (tag == 1) {
            url = "service/del.ddos.port.by.id.php?id=[" + $(trDel).attr("id") + "]";
        } else if (tag == 2) {
            url = "service/del.ddos.domain.by.id.php?id=[" + $(trDel).attr("id") + "]";
        }
        $.ajax({
            url: url,
            type: "get",
            success: function (data) {
                var ret = JSON.parse(data);
                if (ret.hasOwnProperty("code")) {
                    if (ret["code"] == 9001) {
                        //todo
                        window.location.href = "login.php?ref=config_ddos_detail.php" + window.location.search;//check_ddos2.js
                    } else if (ret["code"] == 0) {
                        //todo
                        deleteCurRowHelper(obj, tbl_id, target_id, tag);
                    } else {
                        alert(ret["msg"]);
                    }
                }
            },
            error: function () {
                alert("无法连接服务器");
            }
        });
    } else {

        deleteCurRowHelper(obj, tbl_id, target_id, tag);
    }

}
function deleteCurRowHelper(obj, tbl_id, target_id, tag) {
    var trDel = $(obj).parent().parent();
    var TOTAL = getTotal();//添加协议转发的总条数
    if (tag == 3) {
        TOTAL = getTotalRulesNum();
    }
    var table;
    if (tag == 4) {
        var table = $(obj).parent().parent().parent().parent();
    }
    trDel.remove();
    var tr_length = 0;
    if (tag == 4) {
        tr_length = $(table).find("tbody").children("tr").length;
    } else {
        tr_length = $('#' + tbl_id + '>tbody').children("tr").length;
    }
    var leave = TOTAL - tr_length;
    $('#' + target_id).text(leave);

    if (leave > 0 && tag == 1) {
        $('#btn_proto_forward').removeClass("disabled");
        var content = "您还可以添加<Strong id=\"avail_proto_forward_num\">" + leave + "</Strong>条协议转发规则";
        $('#span_avail_proto_forward_num').html(content);
    } else if (leave > 0 && tag == 2) {
        $('#btn_website_defend_add').removeClass("disabled");
        var content = "您还可以添加<Strong id=\"avail_website_defend_num\">" + leave + "</Strong>条网站防护规则";
        $('#span_website_defend_num').html(content);
    } else if (leave > 0 && tag == 3) {
        $('#btn_rules_add').removeClass("disabled");
        var content = "您还可以添加<Strong id=\"avail_rules_num\">" + leave + "</Strong>条配置规则";
        $('#span_rules_num').html(content);
    } else if (leave > 0 && tag == 4) {
        $(table).next().children("button").removeClass("disabled");
        var span_num = $(table).next().find("span");
        var span_id = $(span_num).attr("id");
        var suffix = span_id.substring(span_id.indexOf("_") + 1);
        var content = "您还可以添加<Strong id=\"avail_domain_acl_num " + suffix + "\">" + leave + "</Strong>域名";
        $(span_num).html(content);
    }
}

function moveCurTrPosition(obj, upOrDownTag) {
    var tbody = $(obj).parent().parent().parent();
    var allRowNum = $(tbody).children("tr").length;
    if (allRowNum == 1) {
        return;
    }
    var curRowNo = $(obj).closest("tr").index();
    //alert(allRowNum + " " + curRowNo);
    if (upOrDownTag == 0 && curRowNo == 0) {
        return;
    }
    if (upOrDownTag == 1 && curRowNo == allRowNum - 1) {
        return;
    }

    var row = $(tbody).children("tr").eq(curRowNo);
    var ruleNameNode = $(row).find("input:first");
    var ruleValueNode = $(row).find('input:last');
    $(ruleNameNode).attr("value", $(ruleNameNode).val());
    $(ruleValueNode).attr("value", $(ruleValueNode).val());
    var rowStr = "<tr>" + row.html() + "</tr>";
    row.remove();
    //alert(rowStr);
    if (upOrDownTag == 0) {
        $(tbody).children("tr").eq(curRowNo - 1).before(rowStr);
    }
    if (upOrDownTag == 1) {
        $(tbody).children("tr").eq(curRowNo).after(rowStr);
    }
}
function showConfigshowModal(tag) {
    $(tag).modal('show');
}
function imgOnMouseOver(obj) {
    $(obj).attr("src", 'images/question_out.png');
    return;
}
function imgOnMouseOut(obj) {
    $(obj).attr("src", 'images/question.png');
}

