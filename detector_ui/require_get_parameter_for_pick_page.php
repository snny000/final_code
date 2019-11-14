<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
?>

<?php
if (isset($_REQUEST["cacheRef"])) {
    ?>
    <script type="text/javascript">
        var cacheRef = "<?php echo $_REQUEST["cacheRef"]?>";
        var cachePage = "<?php echo $_REQUEST["cachePage"]?>";
        //var cacheSearchParam = JSON.parse(<?php echo $_REQUEST["cacheSearchParam"]?>);
        var cacheSearchParam = <?php echo $_REQUEST["cacheSearchParam"]?>;


        var cacheDevice_id_list = eval(<?php echo $_REQUEST["cacheDevice_id_list"]?>);
        
        

        var cacheCmd_type = "<?php echo $_REQUEST["cacheCmd_type"]?>";
        


        var cacheMenu = "<?php echo $_REQUEST["cacheMenu"]?>";
        var cacheType = "<?php echo $_REQUEST["cacheType"]?>";
        var cachePolicy_type = "<?php echo $_REQUEST["cachePolicy_type"]?>";
        var cacheId = eval(<?php echo $_REQUEST["cacheId"]?>);
    </script>
    <?php
} else {
    ?>
    <script type="text/javascript">
        alert("该页面不能直接访问，请按规定流程进行操作！");
        window.location.href = "login.php";
    </script>
    <?php
}
?>