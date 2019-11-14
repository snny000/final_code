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

<?php
if (isset($_REQUEST["warning_module"])) {
    ?>
    <script type="text/javascript">
        var post_warning_module = <?php echo $_REQUEST["warning_module"]?>;
    </script>
    <?php
}
?>

<?php
if (isset($_REQUEST["warning_type"])) {
    ?>
    <script type="text/javascript">
        var post_warning_type = <?php echo $_REQUEST["warning_type"]?>;
    </script>
    <?php
}
?>