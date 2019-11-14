var FRAME = ["<nav class=\"navbar navbar-blue navbar-fixed-top\" role=\"navigation\">",
"        <div class=\"navbar-header navbar-header-fix-height\">",
"          <img class = \"navbar-header-img\" src=\"images/ruizheng.png\">",
"        </div>",
"		<div class=\"navbar-inner\">",
"			<ul class=\"nav navbar-nav navbar-right navbar-user\">",
"				<li class=\"dropdown user-dropdown\">",
"       			<a href=\"#\" class=\"dropdown-toggle\" style=\"padding:10px 10px 11px;height:50px\" data-toggle=\"dropdown\">",
"          			<i class=\"fa fa-user\"></i>",
"          			<div class=\"loginInfo\">",
"            			<span>欢迎您，<span class=\"loginusername\" style=\"font-weight:bold\"></span>",
"              			<br />登录时间:<span class=\"logintime\"></span>",
"            			</span>",
"          			</div>",
"          			<b class=\"caret\"></b>",
"        			</a>",
"              		<ul class=\"dropdown-menu\">",
"                   <li>",
"          <a class=\"switchRole\" style=\"display:none\" href=\"javascript:void(0);\" onclick=\"switch_role();\">",
"          <i class=\"fa fa-cogs\">",
"          </i>",
"          切换角色",
"          </a>",
"        </li>",
"          <li class=\"divider\">",
"          </li>",
"          <li>",
"            <a href=\"javascript:void(0);\" onclick=\"login_out();\">",
"              <i class=\"fa fa-power-off\">",
"              </i>注销</a></li>",
"              		</ul>",
"				</li>",
"			</ul>",
"        	<div class=\"container\">",
"			<div class=\"nav-collapse\">",
"          <ul  id=\"navbar-side\" class=\"nav navbar-nav navbar-right pull-right\">",
"			<li><a id=\"summary\" href=\"summary.php\"> &nbsp&nbsp&nbsp&nbsp首页</a></li>",
"			",
"			<li resourceid='351' class=\"dropdown\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp检测器管理 </a>",
"              <ul class=\"dropdown-menu\">",
"                <li><a resourceid='352' id=\"menu-detector_info\" href=\"detector_info.php\">&nbsp<i class=\"fa fa-search\"></i>&nbsp检测器备案管理</a></li>",
"                <li><a resourceid='352' id=\"menu-detector\" href=\"detector.php\">&nbsp<i class=\"fa fa-code-fork\"></i>&nbsp检测器状态管理</a></li>",
"                <li><a resourceid='352' id=\"menu-detector1\" href=\"detector_online_event.php\">&nbsp<i class=\"fa fa-code-fork\"></i>&nbsp检测器在线事件</a></li>",
"                <li><a resourceid='358' id=\"menu-detector2\" href=\"cmd_audit.php\">&nbsp<i class=\"fa fa-list-alt\"></i>&nbsp检测器本地审计</a></li>",
"              </ul>",
"            </li>",
"			",
"			<li class=\"dropdown\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp告警事件监测 </a>",
"              <ul class=\"dropdown-menu\">",
"                <li><a id=\"menu-alert2\" href=\"stat.php\">&nbsp<i class=\"fa fa-area-chart\"></i>&nbsp告警统计</a></li>",
"                <li><a id=\"menu-alert1\" href=\"alarm.php\">&nbsp<i class=\"fa fa-exclamation-triangle\"></i>&nbsp告警列表</a></li>",
"              </ul>",
"            </li>",
"			",
/*
"			<li class=\"dropdown role role3 role4 role5\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp策略管理 </a>",
"              <ul class=\"dropdown-menu\">",
"                <li class='role role5'><a id=\"menu-rule9\" href=\"rule_group.php\">&nbsp<i class=\"fa fa-suitcase\"></i>&nbsp任务组管理</a></li>",
"                <li class='role role3'><a id=\"menu-rule2\" href=\"rule_trojan.php\">&nbsp<i class=\"fa fa-user-secret\"></i>&nbsp攻击窃密检测策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule3\" href=\"rule_abnormal.php\">&nbsp<i class=\"fa fa-hacker-news\"></i>&nbsp未知攻击检测策略</a></li>",
"                <li class='role role4'><a id=\"menu-rule4\" href=\"rule_keyword_file.php\">&nbsp<i class=\"fa fa-random\"></i>&nbsp传输涉密检测策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule5\" href=\"rule_ip_listen.php\">&nbsp<i class=\"fa fa-file-excel-o\"></i>&nbsp目标审计策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule6\" href=\"rule_net_log.php\">&nbsp<i class=\"fa fa-file-text\"></i>&nbsp网络行为审计策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule7\" href=\"rule_ip_whitelist.php\">&nbsp<i class=\"fa fa-bookmark-o\"></i>&nbspIP白名单策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule8\" href=\"rule_comm_block.php\">&nbsp<i class=\"fa fa-stop-circle \"></i>&nbsp通信阻断策略</a></li>",
"                <li class='role role5'><a id=\"menu-rule1\" href=\"rule_task.php\">&nbsp<i class=\"fa fa-cog\"></i>&nbsp任务查看</a></li>",
"              </ul>",
"            </li>",
*/
"<li class='dropdown role role3 role4'>\
            <a class='for-open' href='#' data-toggle='dropdown' data-stoppropagation='true'>\
              <b class='caret'>\
              </b>\
              &nbsp;策略管理\
            </a>\
            <ul class='dropdown-menu'>\
              <li class='role role4'>\
                <a id='menu-rule9' href='rule_group.php'>\
                  &nbsp;\
                  <i class='fa fa-suitcase'>\
                  </i>\
                  &nbsp;任务组管理\
                </a>\
              </li>\
              <li class='dropdown-submenu'>  \
                    <a resourceid='404' id='menu-rule2' tabindex='-1' href='javascript:;'>\
                     &nbsp;\
                     <i class='fa fa-user-secret'>\
                      </i>\
                      &nbsp;攻击窃密检测策略\
                    </a>  \
                    <ul class='dropdown-menu open'>  \
                        <li>\
                            <a resourceid='359' id='menu-rule2' tabindex='-1' href='rule_trojan.php'>\
                            &nbsp;\
                            <i class='fa fa-certificate'>\
                              </i>\
                              &nbsp;木马攻击检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='361' id='menu-rule2' tabindex='-1' href='rule_attack.php'>\
                            &nbsp;\
                            <i class='fa fa-bug'>\
                              </i>\
                              &nbsp;漏洞利用检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='363' id='menu-rule2' tabindex='-1' href='rule_pefile.php'>\
                            &nbsp;\
                            <i class='fa fa-user-secret'>\
                              </i>\
                              &nbsp;恶意程序检测策略\
                            </a>\
                          </li>\
                    </ul>  \
                </li>\
\
              <li class='role role3'>\
                <a resourceid='365' id='menu-rule3' href='rule_abnormal.php'>\
                  &nbsp;\
                  <i class='fa fa-hacker-news'>\
                  </i>\
                  &nbsp;未知攻击检测策略\
                </a>\
              </li>\
\
              <li class='dropdown-submenu'>  \
                    <a resourceid='405' id='menu-rule4' tabindex='-1' href='javascript:;'>\
                     &nbsp;\
                     <i class='fa fa-random'>\
                      </i>\
                      &nbsp;传输涉密检测策略\
                    </a>  \
                    <ul class='dropdown-menu'>  \
                        <li>\
                            <a resourceid='367' id='menu-rule4' tabindex='-1' href='rule_keyword_file.php'>\
                            &nbsp;\
                            <i class='fa fa-key'>\
                              </i>\
                              &nbsp;关键字检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='369' id='menu-rule4' tabindex='-1' href='rule_encryption_file.php'>\
                            &nbsp;\
                            <i class='fa fa-lock'>\
                              </i>\
                              &nbsp;加密文件检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='371' id='menu-rule4' tabindex='-1' href='rule_compress_file.php'>\
                            &nbsp;\
                            <i class='fa fa-compress'>\
                              </i>\
                              &nbsp;多层压缩检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='373' id='menu-rule4' tabindex='-1' href='rule_picture_file.php'>\
                            &nbsp;\
                            <i class='fa fa-file-image-o'>\
                              </i>\
                              &nbsp;图片筛选策略\
                            </a>\
                          </li>\
                    </ul>  \
              </li>\
\
              <li class='dropdown-submenu'>  \
                    <a resourceid='406' id='menu-rule5' tabindex='-1' href='javascript:;'>\
                     &nbsp;\
                     <i class='fa fa-file-excel-o'>\
                      </i>\
                      &nbsp;目标审计策略\
                    </a>  \
                    <ul class='dropdown-menu'>  \
                        <li>\
                            <a resourceid='375' id='menu-rule5' tabindex='-1' href='rule_ip_listen.php'>\
                            &nbsp;\
                            <i class='fa fa-television'>\
                              </i>\
                              &nbsp;IP审计检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='377' id='menu-rule5' tabindex='-1' href='rule_domain_listen.php'>\
                            &nbsp;\
                            <i class='fa fa-wikipedia-w'>\
                              </i>\
                              &nbsp;域名审计检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='379' id='menu-rule5' tabindex='-1' href='rule_url_listen.php'>\
                            &nbsp;\
                            <i class='fa fa-link'>\
                              </i>\
                              &nbsp;URL审计检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='381' id='menu-rule5' tabindex='-1' href='rule_account_listen.php'>\
                            &nbsp;\
                            <i class='fa fa-file'>\
                              </i>\
                              &nbsp;账号审计检测策略\
                            </a>\
                          </li>\
                    </ul>  \
              </li>\
\
              <li class='dropdown-submenu'>\
                    <a resourceid='407' id='menu-rule6' tabindex='-1' href='javascript:;'>\
                     &nbsp;\
                     <i class='fa fa-file-text'>\
                      </i>\
                      &nbsp;网络行为审计策略\
                    </a>  \
                    <ul class='dropdown-menu'>  \
                        <li>\
                            <a resourceid='383' id='menu-rule6' tabindex='-1' href='rule_net_log.php'>\
                            &nbsp;\
                            <i class='fa fa-upload'>\
                              </i>\
                              &nbsp;通联关系上报策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='385' id='menu-rule6' tabindex='-1' href='rule_app_behavior.php'>\
                            &nbsp;\
                            <i class='fa fa-cloud-upload'>\
                              </i>\
                              &nbsp;应用行为上报策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='387' id='menu-rule6' tabindex='-1' href='rule_web_filter.php'>\
                            &nbsp;\
                            <i class='fa fa-link'>\
                              </i>\
                              &nbsp;应用行为WEB过滤策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='389' id='menu-rule6' tabindex='-1' href='rule_dns_filter.php'>\
                            &nbsp;\
                            <i class='fa fa-fire'>\
                              </i>\
                              &nbsp;应用行为DNS过滤策略\
                            </a>\
                          </li>\
                    </ul>  \
              </li>\
              <li class='role role3'>\
                <a resourceid='391' id='menu-rule7' href='rule_ip_whitelist.php'>\
                  &nbsp;\
                  <i class='fa fa-bookmark-o'>\
                  </i>\
                  &nbsp;IP白名单策略\
                </a>\
              </li>\
              <li class='role role3'>\
                <a resourceid='393' id='menu-rule8' href='rule_comm_block.php'>\
                  &nbsp;\
                  <i class='fa fa-stop-circle '>\
                  </i>\
                  &nbsp;通信阻断策略\
                </a>\
              </li>\
              <li class='role role4'>\
                <a id='menu-rule1' href='rule_task.php'>\
                  &nbsp;\
                  <i class='fa fa-cog'>\
                  </i>\
                  &nbsp;任务查看\
                </a>\
              </li>\
            </ul>\
          </li>",
"			",
"			<li resourceid='395' class=\"dropdown\">",
"              <a resourceid='396' class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp插件管理 </a>",
"              <ul class=\"dropdown-menu\">",
"             	 <li><a id=\"menu-plug1\" href=\"plug.php\">&nbsp<i class=\"fa fa-plug\"></i>&nbsp插件部署管理</a></li>",
"             	 <li><a id=\"menu-plug3\" href=\"plug_alarm.php\">&nbsp<i class=\"fa  fa-product-hunt\"></i>&nbsp插件告警</a></li>",
"             	 <li><a id=\"menu-plug4\" href=\"plug_status.php\">&nbsp<i class=\"fa fa-spinner\"></i>&nbsp插件状态</a></li>",
"             	 <li><a id=\"menu-plug2\" href=\"plug_task.php\">&nbsp<i class=\"fa fa-asterisk\"></i>&nbsp任务查看</a></li>",
"              </ul>",
"            </li>",
"			",
"			<li resourceid='410' class=\"dropdown\">",
"              <a resourceid='410' class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp远程命令 </a>",
"              <ul class=\"dropdown-menu\">",
"             	 <li><a resourceid='410' id=\"menu-order1\" href=\"cmd.php\">&nbsp<i class=\"fa fa-volume-up\"></i>&nbsp命令下发</a></li>",
"                <li><a resourceid='410' id=\"menu-order2\" href=\"cmd_task.php\">&nbsp<i class=\"fa fa-clone\"></i>&nbsp任务查看</a></li>",
"              </ul>",
"            </li>",
"			",
"			<li class=\"dropdown\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp系统管理 </a>",
"              <ul class=\"dropdown-menu\">",
"               <li><a resourceid='281' id=\"menu-account\" href=\"account.php\">&nbsp<i class=\"fa fa-user\"></i>&nbsp账号管理</a></li>",
"               <li><a id=\"menu-passwd\" href=\"change.php\">&nbsp<i class=\"fa fa-key\"></i>&nbsp修改密码</a></li>",
"               <li><a resourceid='277' id=\"menu-role\" href=\"role.php\">&nbsp<i class=\"fa fa-group\"></i>&nbsp角色管理</a></li>",
"               <li><a resourceid='400' id=\"menu-detector3\" href=\"sys_audit.php\">&nbsp<i class=\"fa fa-list-alt\"></i>&nbsp系统审计</a></li>",
"               <li><a resourceid='411' id=\"menu-director\" href=\"director_manage.php\">&nbsp<i class=\"fa fa-edit\"></i>&nbsp指挥配置</a></li>",
"              </ul>",
"            </li>",
"          </ul>",
"		</div>",
"		</div>",
"		</div>",
"        </div><!-- /.navbar-collapse -->",
"      </nav>"].join("");

var FRAME_NARROW = ["<nav class=\"navbar navbar-blue navbar-fixed-top\" role=\"navigation\">",
"        <!-- Brand and toggle get grouped for better mobile display -->",
"        <div class=\"navbar-header navbar-header-fix-height\">",
"          <img class = \"navbar-header-img\" src=\"images/ruizheng.png\">",
"        </div>",
"        <!-- Collect the nav links, forms, and other content for toggling -->",
"        <div  class=\"collapse navbar-collapse navbar-ex1-collapse\">",
"          <ul  id=\"navbar-side\" class=\"nav navbar-nav side-nav\">",
"			<li><a id=\"summary\" href=\"summary.php\"> &nbsp&nbsp&nbsp&nbsp首页</a></li>",
"			",
"			<li class=\"dropdown open\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp检测器管理 </a>",
"              <ul class=\"dropdown-menu\">",
"                <li><a id=\"menu-detector_info\" href=\"detector_info.php\">&nbsp<i class=\"fa fa-search\"></i>&nbsp检测器信息管理</a></li>",
"                <li><a id=\"menu-detector\" href=\"detector.php\">&nbsp<i class=\"fa fa-code-fork\"></i>&nbsp检测器状态管理</a></li>",
"                <li><a id=\"menu-detector1\" href=\"detector_online_event.php\">&nbsp<i class=\"fa fa-code-fork\"></i>&nbsp检测器在线事件</a></li>",
"                <li><a id=\"menu-detector2\" href=\"cmd_audit.php\">&nbsp<i class=\"fa fa-list-alt\"></i>&nbsp检测器本地审计</a></li>",
"              </ul>",
"            </li>",
    "			<li class=\"dropdown open\">",
    "              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp告警事件监测 </a>",
    "              <ul class=\"dropdown-menu\">",
    "                <li><a id=\"menu-alert1\" href=\"alarm.php\">&nbsp<i class=\"fa fa-exclamation-triangle\"></i>&nbsp告警列表</a></li>",
    "                <li><a id=\"menu-alert2\" href=\"stat.php\">&nbsp<i class=\"fa fa-area-chart\"></i>&nbsp告警统计</a></li>",
    "              </ul>",
    "            </li>",
    "			",
"			",
/*"			<li class=\"dropdown open role role3 role4 role5\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp策略管理 </a>",
"              <ul class=\"dropdown-menu\">",
"                <li class='role role5'><a id=\"menu-rule1\" href=\"rule_task.php\">&nbsp<i class=\"fa fa-cog\"></i>&nbsp任务查看</a></li>",
"                <li class='role role3'><a id=\"menu-rule2\" href=\"rule_trojan.php\">&nbsp<i class=\"fa fa-user-secret\"></i>&nbsp攻击窃密检测策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule3\" href=\"rule_abnormal.php\">&nbsp<i class=\"fa fa-hacker-news\"></i>&nbsp未知攻击检测策略</a></li>",
"                <li class='role role4'><a id=\"menu-rule4\" href=\"rule_keyword_file.php\">&nbsp<i class=\"fa fa-random\"></i>&nbsp传输涉密检测策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule5\" href=\"rule_ip_listen.php\">&nbsp<i class=\"fa fa-file-excel-o\"></i>&nbsp目标审计策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule6\" href=\"rule_net_log.php\">&nbsp<i class=\"fa fa-file-text\"></i>&nbsp网络行为审计策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule7\" href=\"rule_ip_whitelist.php\">&nbsp<i class=\"fa fa-bookmark-o\"></i>&nbspIP白名单策略</a></li>",
"                <li class='role role3'><a id=\"menu-rule8\" href=\"rule_comm_block.php\">&nbsp<i class=\"fa fa-stop-circle \"></i>&nbsp通信阻断策略</a></li>",
"              </ul>",
"            </li>",
*/
"<li class='dropdown open role role3 role4'>\
            <a class='for-open' href='#' data-toggle='dropdown' data-stoppropagation='true'>\
              <b class='caret'>\
              </b>\
              &nbsp;策略管理\
            </a>\
            <ul class='dropdown-menu'>\
              <li class='role role4'>\
                <a id='menu-rule9' href='rule_group.php'>\
                  &nbsp;\
                  <i class='fa fa-suitcase'>\
                  </i>\
                  &nbsp;任务组管理\
                </a>\
              </li>\
              <li class='dropdown-submenu open'>  \
                    <a resourceid='404' id='menu-rule2' tabindex='-1' href='javascript:;'>\
                     &nbsp;\
                     <i class='fa fa-user-secret'>\
                      </i>\
                      &nbsp;攻击窃密检测策略\
                    </a>  \
                    <ul class='dropdown-menu open'>  \
                        <li>\
                            <a resourceid='359' id='menu-rule2' tabindex='-1' href='rule_trojan.php'>\
                            &nbsp;\
                            <i class='fa fa-certificate'>\
                              </i>\
                              &nbsp;木马攻击检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='361' id='menu-rule2' tabindex='-1' href='rule_attack.php'>\
                            &nbsp;\
                            <i class='fa fa-bug'>\
                              </i>\
                              &nbsp;漏洞利用检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='363' id='menu-rule2' tabindex='-1' href='rule_pefile.php'>\
                            &nbsp;\
                            <i class='fa fa-user-secret'>\
                              </i>\
                              &nbsp;恶意程序检测策略\
                            </a>\
                          </li>\
                    </ul>  \
                </li>\
\
              <li class='role role3'>\
                <a resourceid='365' id='menu-rule3' href='rule_abnormal.php'>\
                  &nbsp;\
                  <i class='fa fa-hacker-news'>\
                  </i>\
                  &nbsp;未知攻击检测策略\
                </a>\
              </li>\
\
              <li class='dropdown-submenu open'>  \
                    <a resourceid='405' id='menu-rule4' tabindex='-1' href='javascript:;'>\
                     &nbsp;\
                     <i class='fa fa-random'>\
                      </i>\
                      &nbsp;传输涉密检测策略\
                    </a>  \
                    <ul class='dropdown-menu'>  \
                        <li>\
                            <a resourceid='367' id='menu-rule4' tabindex='-1' href='rule_keyword_file.php'>\
                            &nbsp;\
                            <i class='fa fa-key'>\
                              </i>\
                              &nbsp;关键字检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='369' id='menu-rule4' tabindex='-1' href='rule_encryption_file.php'>\
                            &nbsp;\
                            <i class='fa fa-lock'>\
                              </i>\
                              &nbsp;加密文件检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='371' id='menu-rule4' tabindex='-1' href='rule_compress_file.php'>\
                            &nbsp;\
                            <i class='fa fa-compress'>\
                              </i>\
                              &nbsp;多层压缩检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='373' id='menu-rule4' tabindex='-1' href='rule_picture_file.php'>\
                            &nbsp;\
                            <i class='fa fa-file-image-o'>\
                              </i>\
                              &nbsp;图片筛选策略\
                            </a>\
                          </li>\
                    </ul>  \
              </li>\
\
              <li class='dropdown-submenu open'>  \
                    <a resourceid='406' id='menu-rule5' tabindex='-1' href='javascript:;'>\
                     &nbsp;\
                     <i class='fa fa-file-excel-o'>\
                      </i>\
                      &nbsp;目标审计策略\
                    </a>  \
                    <ul class='dropdown-menu'>  \
                        <li>\
                            <a resourceid='375' id='menu-rule5' tabindex='-1' href='rule_ip_listen.php'>\
                            &nbsp;\
                            <i class='fa fa-television'>\
                              </i>\
                              &nbsp;IP审计检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='377' id='menu-rule5' tabindex='-1' href='rule_domain_listen.php'>\
                            &nbsp;\
                            <i class='fa fa-wikipedia-w'>\
                              </i>\
                              &nbsp;域名审计检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='379' id='menu-rule5' tabindex='-1' href='rule_url_listen.php'>\
                            &nbsp;\
                            <i class='fa fa-link'>\
                              </i>\
                              &nbsp;URL审计检测策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='381' id='menu-rule5' tabindex='-1' href='rule_account_listen.php'>\
                            &nbsp;\
                            <i class='fa fa-file'>\
                              </i>\
                              &nbsp;账号审计检测策略\
                            </a>\
                          </li>\
                    </ul>  \
              </li>\
\
              <li class='dropdown-submenu open'>\
                    <a resourceid='407' id='menu-rule6' tabindex='-1' href='javascript:;'>\
                     &nbsp;\
                     <i class='fa fa-file-text'>\
                      </i>\
                      &nbsp;网络行为审计策略\
                    </a>  \
                    <ul class='dropdown-menu'>  \
                        <li>\
                            <a resourceid='383' id='menu-rule6' tabindex='-1' href='rule_net_log.php'>\
                            &nbsp;\
                            <i class='fa fa-upload'>\
                              </i>\
                              &nbsp;通联关系上报策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='385' id='menu-rule6' tabindex='-1' href='rule_app_behavior.php'>\
                            &nbsp;\
                            <i class='fa fa-cloud-upload'>\
                              </i>\
                              &nbsp;应用行为上报策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='387' id='menu-rule6' tabindex='-1' href='rule_web_filter.php'>\
                            &nbsp;\
                            <i class='fa fa-link'>\
                              </i>\
                              &nbsp;应用行为WEB过滤策略\
                            </a>\
                          </li>\
                          <li>\
                            <a resourceid='389' id='menu-rule6' tabindex='-1' href='rule_dns_filter.php'>\
                            &nbsp;\
                            <i class='fa fa-fire'>\
                              </i>\
                              &nbsp;应用行为DNS过滤策略\
                            </a>\
                          </li>\
                    </ul>  \
              </li>\
              <li class='role role3'>\
                <a resourceid='391' id='menu-rule7' href='rule_ip_whitelist.php'>\
                  &nbsp;\
                  <i class='fa fa-bookmark-o'>\
                  </i>\
                  &nbsp;IP白名单策略\
                </a>\
              </li>\
              <li class='role role3'>\
                <a resourceid='393' id='menu-rule8' href='rule_comm_block.php'>\
                  &nbsp;\
                  <i class='fa fa-stop-circle '>\
                  </i>\
                  &nbsp;通信阻断策略\
                </a>\
              </li>\
              <li class='role role4'>\
                <a id='menu-rule1' href='rule_task.php'>\
                  &nbsp;\
                  <i class='fa fa-cog'>\
                  </i>\
                  &nbsp;任务查看\
                </a>\
              </li>\
            </ul>\
          </li>",
"			",
"			<li class=\"dropdown open\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp插件管理 </a>",
"              <ul class=\"dropdown-menu\">",
"             	 <li><a id=\"menu-plug1\" href=\"plug.php\">&nbsp<i class=\"fa fa-plug\"></i>&nbsp插件部署管理</a></li>",
"             	 <li><a id=\"menu-plug2\" href=\"plug_cmd.php\">&nbsp<i class=\"fa fa-asterisk\"></i>&nbsp插件命令管理</a></li>",
"             	 <li><a id=\"menu-plug3\" href=\"plug_alarm.php\">&nbsp<i class=\"fa  fa-product-hunt\"></i>&nbsp插件告警</a></li>",
"             	 <li><a id=\"menu-plug4\" href=\"plug_status.php\">&nbsp<i class=\"fa fa-spinner\"></i>&nbsp插件状态</a></li>",
"              </ul>",
"            </li>",
"			",
"			<li class=\"dropdown open\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp远程命令 </a>",
"              <ul class=\"dropdown-menu\">",
"                <li><a id=\"menu-order2\" href=\"cmd_task.php\">&nbsp<i class=\"fa fa-clone\"></i>&nbsp任务查看</a></li>",
"             	 <li><a id=\"menu-order1\" href=\"cmd.php\">&nbsp<i class=\"fa fa-volume-up\"></i>&nbsp命令下发</a></li>",
"              </ul>",
"            </li>",
"			",
"			<li class=\"dropdown open\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp系统管理 </a>",
"              <ul class=\"dropdown-menu\">",
    "               <li><a id=\"menu-account\" href=\"account.php\">&nbsp<i class=\"fa fa-user\"></i>&nbsp账号管理</a></li>",
    "               <li><a id=\"menu-passwd\" href=\"change.php\">&nbsp<i class=\"fa fa-key\"></i>&nbsp修改密码</a></li>",
    "               <li><a id=\"menu-role\" href=\"role.php\">&nbsp<i class=\"fa fa-group\"></i>&nbsp角色管理</a></li>",
    "               <li><a id=\"menu-detector3\" href=\"sys_audit.php\">&nbsp<i class=\"fa fa-list-alt\"></i>&nbsp系统审计</a></li>",
    "               <li><a id=\"menu-director\" href=\"director_manage.php\">&nbsp<i class=\"fa fa-edit\"></i>&nbsp指挥配置</a></li>",
"              </ul>",
"            </li>",
"          </ul>",
"          <ul class=\"nav navbar-nav navbar-right navbar-user\">",
"            <li class=\"dropdown user-dropdown\">",
"       			<a href=\"#\" class=\"dropdown-toggle\" style=\"padding:10px 10px 11px;height:50px\" data-toggle=\"dropdown\">",
"          			<i class=\"fa fa-user\"></i>",
"          			<div class=\"loginInfo\">",
"            			<span>欢迎您，<span class=\"loginusername\" style=\"font-weight:bold\"></span>",
"              			<br />登录时间:<span class=\"logintime\"></span>",
"            			</span>",
"          			</div>",
"          			<b class=\"caret\"></b>",
"        			</a>",
"              		<ul class=\"dropdown-menu\">",
"                   <li>",
"          <a class=\"switchRole\" style=\"display:none\" href=\"javascript:void(0);\" onclick=\"switch_role();\">",
"          <i class=\"fa fa-cogs\">",
"          </i>",
"          切换角色",
"          </a>",
"        </li>",
"                		<li class=\"divider\"></li>",
"                		<li><a href=\"javascript:void(0);\" onclick=\"login_out();\"><i class=\"fa fa-power-off\"></i> 注销</a></li>",
"              		</ul>",
"				</li>",
"          </ul>",
"        </div><!-- /.navbar-collapse -->",
"      </nav>"].join("");

var COPYRIGHT = ["<div class=\"copyright\">",
"                <p>COPYRIGHT@2016 ##############公司版权所有 </p>",
"                <p>公司地址:#################### 24小时电话服务热线：4009-####-##</p>",
//"                <p>备案号：京ICP备*******号</p>",
"            </div>"].join("");

$(function() {	
	//sidebar-closable
	$('.side-nav .dropdown').each(function(){
		this.closable = false;
	});


	$('.side-nav .for-open').click(function(){
		console.log("----------for-open----------")
		console.log(this.parentNode)
		this.parentNode.closable = true;
	});


	$('.side-nav .dropdown').on({
		"shown.bs.dropdown": function() { this.closable = false; },
		"hide.bs.dropdown":  function() { return this.closable; }
	});

	//active-blue
	//$('#menu-ddos').css("background","#09C");
	//$('#menu-ddos').css("color","#fff");
	//search-closable
	$('.search-dropdown input').focus(function(){		
		this.parentNode.parentNode.parentNode.parentNode.closable = false;
	});
	$('.search-dropdown button').focus(function(){			
		this.parentNode.parentNode.parentNode.parentNode.parentNode.closable = false;
	});
	$('.search-dropdown input').blur(function(){		
		this.parentNode.parentNode.parentNode.parentNode.closable = true;
	});
	$('.search-dropdown button').blur(function(){			
		this.parentNode.parentNode.parentNode.parentNode.parentNode.closable = true;
	});
	$('.search-dropdown').on({
		"hide.bs.dropdown":  function() { return this.closable; }
	});
	
	$('.search-dropdown button').blur(function(){
		this.parentNode.parentNode.parentNode.parentNode.parentNode.closable = true;
	});

});

// function buildFrame(activeElement){
// 	$('#whole-wrapper').prepend(FRAME);
// 	if(activeElement.length){
// 		$('#navbar-side').animate({scrollTop:$('#'+activeElement).offset().top-100},10)
// 		$('#'+activeElement).css("background","#09C");
// 		$('#'+activeElement).css("color","#fff");
// 	}
// 	if(localStorage.level==0){
// 		//$("#change").hide()
// 		//$(".role").hide();
// 		$(".role").show();
// 	}else if(localStorage.level==1){
// 		//$("#change").hide()
// 		$(".role").hide();
// 	}else if(localStorage.level==2){
// 		$(".role").hide();
// 	}else if(localStorage.level==3){
// 		$(".role").hide();
// 		$(".role3").show();
// 	}else if(localStorage.level==4){
// 		$(".role").hide();
// 		$(".role4").show();

// 	}else if(localStorage.level==5){
// 		$(".role").hide();
// 		$(".role5").show();

// 	}else if(localStorage.level==6){
// 		$(".role").hide();

// 	}else{
// 		$(".role").hide();

// 	}

// 	console.log($('#'+activeElement).css('display'))
// 	if($('#'+activeElement).parent().css('display')=='none'){
// 		alert("越权访问！");
// 		login_out();
// 		//localStorage.clear();
// 		//window.location.href="login.php";/////SESSION验证

// 	}

// }


$('#whole-wrapper').on('click','.dropdown-submenu>a',function(){
    var currHref =  $(this).next().find('li a').attr('href');
    $(this).attr("href",currHref);
})


var currentActiveElement = "";
function buildFrame(activeElement,reset){
	currentActiveElement = activeElement;
	if(reset == 'reset'){
		if (activeElement.length) {
			$('#' + activeElement).css("background", "rgb(0,142,190)");
			$('#' + activeElement).css("color", "#fff");
			// 横向导航栏突出当前操作的菜单
			if($(window).width() > 1024 ){
				var rootNav = $('#' + activeElement).parent().parent().prev();
				if(rootNav.length == 0){
					$('#' + activeElement).css('border-bottom','3px solid #ff7f74');
					$('#' + activeElement).css("background", "rgb(0,142,190)");
				}else{
					rootNav.css('border-bottom','3px solid #ff7f74');
					rootNav.css("background", "rgb(0,142,190)");
				}
			}
		}
		return;
	}
	if ($(window).width() < 1024) {
		$('#whole-wrapper').prepend(FRAME_NARROW);
		$("#whole-wrapper").css("padding-left", 180);
    $('.dropdown-submenu > .dropdown-menu').css('left','5%');
	} else {
		$('#whole-wrapper').prepend(FRAME);
		$("#whole-wrapper").css("padding-left", 0);
    $('.dropdown-submenu > .dropdown-menu').css('left','100%');
	} if (activeElement.length) {
		$('#' + activeElement).css("background", "rgb(0,142,190)");
		$('#navbar-side').animate({ scrollTop: $('#' + activeElement).offset().top - 100 }, 10)
		/*$('#' + activeElement).css("background", "#09C");*/
		
		$('#' + activeElement).css("color", "#fff");
		// 横向导航栏突出当前操作的菜单
		if($(window).width() > 1024 ){
			var rootNav = $('#' + activeElement).parent().parent().prev();
			if(rootNav.length == 0){
				$('#' + activeElement).css('border-bottom','3px solid #ff7f74');
				$('#' + activeElement).css("background", "rgb(0,142,190)");
			}else{
				rootNav.css('border-bottom','3px solid #ff7f74');
				rootNav.css("background", "rgb(0,142,190)");
			}
		}
	}
	// if(localStorage.level==0){
	// 	//$("#change").hide()
	// 	//$(".role").hide();
	// 	$(".role").show();
	// }else if(localStorage.level==1){
	// 	//$("#change").hide()
	// 	$(".role").hide();
	// }else if(localStorage.level==2){
	// 	$(".role").hide();
	// }else if(localStorage.level==3){
	// 	$(".role").hide();
	// 	$(".role3").show();
	// }else if(localStorage.level==4){
	// 	$(".role").hide();
	// 	$(".role4").show();

	// }else if(localStorage.level==5){
	// 	$(".role").hide();
	// 	$(".role5").show();

	// }else if(localStorage.level==6){
	// 	$(".role").hide();

	// }else{
	// 	$(".role").hide();

	// }

	// console.log($('#'+activeElement).css('display'))
	// if($('#'+activeElement).parent().css('display')=='none'){
	// 	alert("越权访问！");
	// 	login_out();
	// 	//localStorage.clear();
	// 	//window.location.href="login.php";/////SESSION验证

	// }

}



function setFrameValue(msgList, uuid, sealMsgNum, visibleNum){
	$('.user-dropdown a span').html(uuid);
	var msgHtml = "";
	var count = 0;
	for (var i in msgList){
		msgHtml += "<li class=\"message-preview\"><a href=\"message_detail.php?id="+msgList[i].id+"\"><span class=\"name\">"+msgList[i].title+"</span><span class=\"message\">"+cutMessage(msgList[i].content)+"</span><span class=\"time\"><i class=\"fa fa-clock-o\"></i>"+msgList[i].create_time+"</span></a></li>";
		msgHtml += "<li class=\"divider\"></li>";
		count++;
		if(count>=visibleNum){
			break;
		}
	}
	$('#msg-divider').after(msgHtml);
	$('li.messages-dropdown > a > span').html(sealMsgNum);

}

function setNewsValue(newsList){
	var newsHtml = "";
	for (var i in newsList){
		var headNews = "";
		if(newsList[i].is_top = 1){
			headNews = "<span class=\"head-news\">头条</span>";
		}
		newsHtml += "<li><a href=\""+newsList[i].url+"\">"+headNews+"  &nbsp"+newsList[i].title+"</a></li>";
	}
	$('.work-news ul').html(newsHtml);
}

function cutMessage(msg){
	if(msg.length<50){
		return msg;
	} else {
		return msg.substring(0,49) + "......";
	}
}

function login_out(){
	$.ajax({
		//url: "/ajax_action_detector.php?uu=login.check",/////本地验证
		url: "/ajax_action_detector.php?uu=login.user_logout",/////SESSION验证
		type: "post",
		data: { username: localStorage.loginid},
		success:function(data) {
			var res = JSON.parse(data);
			if(res["code"]==200){

				localStorage.clear();
				window.location.href="logout.php";/////SESSION验证


			} else {
				alert(res["msg"]);

			}
		},
		error: function () {
			alert("无法连接服务器");
		},

	});
	////不用的///window.location.href="login.php";/////本地验证
	//window.location.href="logout.php";/////SESSION验证

}


	/* 监听浏览器窗口变化更换导航栏位置 */
$(window).resize(function(){
	if($(window).width() < 1024){
		$("#whole-wrapper .navbar-fixed-top").remove();
		$('#whole-wrapper').prepend(FRAME_NARROW);
		$("#whole-wrapper").css("padding-left",180);
    $('.dropdown-submenu > .dropdown-menu').css('left','5%');
		initRoleResource();
	}else{
		$("#whole-wrapper .navbar-fixed-top").remove();
		$('#whole-wrapper').prepend(FRAME);
		$("#whole-wrapper").css("padding-left",0);
    $('.dropdown-submenu > .dropdown-menu').css('left','100%');
		initRoleResource(); 
	}
	buildFrame(currentActiveElement,'reset');
})

var initRoleResource = function () {
	var levelMap = {
		0:'超级管理员',
		1:'系统管理员',
		2:'安全保密管理员',
		3:'策略配置人员',
		4:'传输涉密配置人员',
		5:'策略审计人员',
		6:'普通运维用户'
	};
	var roleResourceIds = JSON.parse(localStorage.getItem('roleResourceIds'));
    $.each($('a[resourceid],div[resourceid],button[resourceid],li[resourceid]'), function (i, a) {
		if (roleResourceIds.indexOf(parseInt($(this).attr('resourceid'))) == - 1) {
			//$(this).attr('style', 'display:none');
			$(this).remove();
		}
	});
	$('.loginusername').text(localStorage.loginid + '('+localStorage.currentRole+')');
	$('.logintime').text(localStorage.timestamp);
}
window.onload = function () {
  initRoleResource();
};

var switchRoleModal = `<div class="modal fade" id="switchRole" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    选择角色
                </h4>
            </div>
            <div class="modal-body">
                <div>
                    
                </div>

            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-interval btn-primary" onclick="switchSubmit()">确定</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div>
    </div>
</div>`
$('body').append(switchRoleModal);


$(function(){
  var roles = JSON.parse(localStorage.roles);
  var rolecount = 0;
  for(var key in roles){
    rolecount++;
  }
  if(rolecount>1){
    setTimeout(function(){
      $('.switchRole').show();
    },2000)
  }
})
function switch_role(){
  var roles = JSON.parse(localStorage.roles);
  var radio = "";
  for(var key in roles){
      radio += '<label><input type="radio" name="switch_role" value='+JSON.stringify(roles[key])+'>'+key+'</label>'
  }
  $('#switchRole .modal-body div').html(radio);
  var radios = $('input[name=switch_role]').parent();
  $.each(radios,function(i){
    if($(radios[i]).text() == localStorage.currentRole){
        $(radios[i]).find('input[type=radio]').prop('checked','checked');
    }
  })
  $('#switchRole').modal('show');
}
function switchSubmit(){
    var roleResourceIds = $('input[name=switch_role]:checked').attr('value');
    if(roleResourceIds == undefined){
        alert('请选择角色');
        return;
    }
    localStorage.roleResourceIds = roleResourceIds;
    localStorage.currentRole = $('input[name=switch_role]:checked').parent().text();
    window.location.href="summary.php";
}
/*http://fontawesome.io/icons/*/