<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
?>
<?php
if (isset($_REQUEST["cachePage"])) {
    //putLog("11111111111111111".$_REQUEST["cacheSearchParam"]);
    ?>
    <script type="text/javascript">
        var cachePage = "<?php echo $_REQUEST["cachePage"]?>";
        //var cacheSearchParam = JSON.parse(<?php echo $_REQUEST["cacheSearchParam"]?>);
        var cacheSearchParam = <?php echo $_REQUEST["cacheSearchParam"]?>;
    </script>
    <?php
} else if(isset($_REQUEST["addIntoGroup"])) {
    ?>
    <script type="text/javascript">
        var cachePage = 1;
        var cacheSearchParam = {random:1};
        var addIntoGroup = <?php echo $_REQUEST["addIntoGroup"]?>;
    </script>
    <?php
}
 else {
    ?>
    <script type="text/javascript">
        var cachePage = 1;
        var cacheSearchParam = {random:1};
        var addIntoGroup = {state:undefined};
    </script>
    <?php
}
?>





<?php
if (isset($_REQUEST["device_id"])) {
    ?>
    <script type="text/javascript">
        var post_device_id = <?php echo $_REQUEST["device_id"]?>;
    </script>
    <?php
}
?>
<?php
if (isset($_REQUEST["center_id"])) {
    ?>
    <script type="text/javascript">
        var post_center_id = <?php echo $_REQUEST["center_id"]?>;
    </script>
    <?php
}
?>