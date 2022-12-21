<div id="done"> </div>
<!-- widget grid -->
<section id="widget-grid" class="">

	<!-- row -->
	<div class="row">

        <!-- NEW WIDGET START -->
		<article class="col-xs-12 col-sm-12 col-md-12 col-lg-12">

            <!-- Widget ID (each widget will need unique ID)-->
            <div class="jarviswidget jarviswidget-color-blueDark" id="wid-id-0"
                data-widget-editbutton="false"
				data-widget-colorbutton="false"
				data-widget-deletebutton="false"
				data-widget-togglebutton="false"
				data-widget-sortable="false"
                data-widget-fullscreenbutton="false">

                <header>
                    <span class="widget-icon"> <i class="fa fa-table"></i> </span>
                    <h2>Content</h2>

                </header>

                <!-- widget div-->
                <div>
                    <div class="widget-body no-padding">
                        <form id="event-form" class="smart-form">
                            <fieldset>
                                <div class="row">
                                    <section class="col col-3">
                                        <label class="label">Event ID</label>
                                        <label class="input state-success"> <i class="icon-prepend fa fa-barcode"></i>
                                            <input type="text" name="event" value="<?=$event_item->event?>" readonly="readonly">
                                        </label>
                                    </section>
                                    <section class="col col-3">
                                        <label class="label">Date</label>
                                        <label class="input state-success"> <i class="icon-prepend fa  fa-calendar"></i>
                                            <input type="tel" name="date" value="<?=$event_item->date?>" data-mask="9999-99-99">
                                        </label>
                                    </section>
                                    <section class="col col-3">
                                        <label class="label">Site</label>
                                        <label class="input state-success"> <i class="icon-prepend fa fa-location-arrow"></i>
                                            <input type="text" name="site" value="<?=$event_item->site?>">
                                        </label>
                                    </section>
                                </div>
                                <section>
                                    <label class="label">Remark</label>
                                    <label class="textarea state-info" >
                                        <textarea rows="4" name="remark"><?=$event_item->remark?></textarea>
                                    </label>
                                </section>
                            </fieldset>

                            <footer>
                                <button type="submit" class="btn btn-default">Update</button>
                            </footer>
                        </form>
                    </div>
                </div>
                <!-- end widget div -->
            </div>
            <!-- end widget -->
        </article>
        <!-- WIDGET END -->
    </div>

    <!-- row -->
	<div class="row">
		<!-- NEW WIDGET START -->
		<article class="col-xs-12 col-sm-12 col-md-12 col-lg-4">

			<!-- Widget ID (each widget will need unique ID)-->
			<div class="jarviswidget jarviswidget-color-write" id="wid-id-1" data-widget-editbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
				<!-- widget options:
				usage: <div class="jarviswidget" id="wid-id-0" data-widget-editbutton="false">
				-->
				<header>
					<span class="widget-icon"> <i class="fa fa-table"></i> </span>
					<h2>Data-Beacon</h2>

				</header>

				<!-- widget div-->
				<div>
					<!-- widget content -->
					<div class="widget-body">
                        <?php if ($data_beacon){?>
                        <p>
                            field: <code>uuid, mac, major, minor, rssi, receiver, ts</code>
                        </p>
                        <p>
                            length: <code><?= count($data_beacon)?></code>
                        </p>
                        <p>
                            ts: <code>
                                <?= $data_beacon[0]->ts?>
                                - 
                                <?= end($data_beacon)->ts?>
                            </code>
                        </p>
                        <p>
                            date: <code>
                                <?= date("Y-m-d H:i", $data_beacon[0]->ts / 1000) ?>
                                -
                                <?= date("Y-m-d H:i", end($data_beacon)->ts / 1000) ?>
                            </code>
						</p>
						<hr class="simple">
						<p>
                            api: <a href="<?= base_url()."/public/survey/api_data/survey_beacon/".$event->event_id?>"><code>link</code></a>
                        </p>
                        <p>
                            csv: <a href="survey/download/survey_beacon/<?=$event->event_id?>" class="btn btn-xs bg-color-blue txt-color-white">beacon: <?= $event->event_id?></a>
                        </p>
                        <?php }else{?>
                        <p>No Data</p>
                        <?php }?>
					</div>
					<!-- end widget content -->
                    
				</div>
				<!-- end widget div -->

			</div>
			<!-- end widget -->
        </article>
        <!-- NEW WIDGET START -->
		<article class="col-xs-12 col-sm-12 col-md-12 col-lg-4">

            <!-- Widget ID (each widget will need unique ID)-->
            <div class="jarviswidget jarviswidget-color-write" id="wid-id-3" data-widget-editbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
                <!-- widget options:
                usage: <div class="jarviswidget" id="wid-id-0" data-widget-editbutton="false">
                -->
                <header>
                    <span class="widget-icon"> <i class="fa fa-table"></i> </span>
                    <h2>Data-Wi-Fi</h2>

                </header>

                <!-- widget div-->
                <div>
                    <!-- widget content -->
                    <div class="widget-body">
                        <?php if ($data_wifi){?>
                        <p>
                            field: <code>src_type, bssid, ssid, rssi, ch, receiver, ts</code>
                        </p>
                        <p>
                            length: <code><?= count($data_wifi)?></code>
                        </p>
                        <p>
                            ts: <code>
                                <?= $data_wifi[0]->ts?>
                                - 
                                <?= end($data_wifi)->ts?>
                            </code>
                        </p>
                        <p>
                            date: <code>
                                <?= date("Y-m-d H:i", $data_wifi[0]->ts / 1000) ?>
                                -
                                <?= date("Y-m-d H:i", end($data_wifi)->ts / 1000) ?>
                            </code>
						</p>
                        <hr class="simple">
                        <p>
                            api: <a href="<?= base_url()."/public/survey/api_data/survey_wifi/".$event->event_id?>"><code>link</code></a>
                        </p>
                        <p>
                            csv: <a href="survey/download/survey_wifi/<?=$event->event_id?>" class="btn btn-xs bg-color-blue txt-color-white">wi-fi: <?= $event->event_id?></a>
                        </p>
                        <?php }else{?>
                        <p>No Data</p>
                        <?php }?>
                    </div>
                    <!-- end widget content -->
                    
                </div>
                <!-- end widget div -->

            </div>
            <!-- end widget -->
        </article>

        <article class="col-xs-12 col-sm-12 col-md-12 col-lg-4">

            <!-- Widget ID (each widget will need unique ID)-->
            <div class="jarviswidget jarviswidget-color-write" id="wid-id-5" data-widget-editbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
                <!-- widget options:
                usage: <div class="jarviswidget" id="wid-id-0" data-widget-editbutton="false">
                -->
                <header>
                    <span class="widget-icon"> <i class="fa fa-table"></i> </span>
                    <h2>Data-imu</h2>

                </header>

                <!-- widget div-->
                <div>
                    <!-- widget content -->
                    <div class="widget-body">
                        <?php if ($data_imu){?>
                        <p>
                            field: <code>a, w, h, A, receiver, ts</code>
                        </p>
                        <p>
                            length: <code><?= count($data_imu)?></code>
                        </p>
                        <p>
                            ts: <code>
                                <?= $data_imu[0]->ts?>
                                - 
                                <?= end($data_imu)->ts?>
                            </code>
                        </p>
                        <p>
                            date: <code>
                                <?= date("Y-m-d H:i", $data_imu[0]->ts / 1000) ?>
                                -
                                <?= date("Y-m-d H:i", end($data_imu)->ts / 1000) ?>
                            </code>
						</p>
                        <hr class="simple">
                        <p>
                            api: <a href="<?= base_url()."/public/survey/api_data/survey_imu/".$event->event_id?>"><code>link</code></a>
                        </p>
                        <p>
                            csv: <a href="survey/download/survey_imu/<?=$event->event_id?>"s class="btn btn-xs bg-color-blue txt-color-white">imu: <?= $event->event_id?></a>
                        </p>
                        <?php }else{?>
                        <p>No Data</p>
                        <?php }?>
                    </div>
                    <!-- end widget content -->
                    
                </div>
                <!-- end widget div -->

            </div>
            <!-- end widget -->
        </article>
        <!-- NEW WIDGET START -->

        <article class="col-xs-12 col-sm-12 col-md-12 col-lg-4">

            <!-- Widget ID (each widget will need unique ID)-->
            <div class="jarviswidget jarviswidget-color-write" id="wid-id-4" data-widget-editbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
                <!-- widget options:
                usage: <div class="jarviswidget" id="wid-id-0" data-widget-editbutton="false">
                -->
                <header>
                    <span class="widget-icon"> <i class="fa fa-table"></i> </span>
                    <h2>Data-uwb_dist</h2>

                </header>

                <!-- widget div-->
                <div>
                    <!-- widget content -->
                    <div class="widget-body">
                        <?php if ($data_uwb_dist){?>
                        <p>
                            field: <code>tag_id, anchor_id, dist_raw, dist_calibration, seq, receiver, ts</code>
                        </p>
                        <p>
                            length: <code><?= count($data_uwb_dist)?></code>
                        </p>
                        <p>
                            ts: <code>
                                <?= $data_uwb_dist[0]->ts?>
                                - 
                                <?= end($data_uwb_dist)->ts?>
                            </code>
                        </p>
                        <p>
                            date: <code>
                                <?= date("Y-m-d H:i", $data_uwb_dist[0]->ts / 1000) ?>
                                -
                                <?= date("Y-m-d H:i", end($data_uwb_dist)->ts / 1000) ?>
                            </code>
						</p>
                        <hr class="simple">
                        <p>
                            api: <a href="<?= base_url()."/public/survey/api_data/survey_uwb_dist/".$event->event_id?>"><code>link</code></a>
                        </p>
                        <p>
                            csv: <a href="survey/download/survey_uwb_dist/<?=$event->event_id?>" class="btn btn-xs bg-color-blue txt-color-white">uwb_dist: <?= $event->event_id?></a>
                        </p>
                        <?php }else{?>
                            <p>No Data</p>
                        <?php }?>
                    </div>
                    <!-- end widget content -->
                    
                </div>
                <!-- end widget div -->

            </div>
            <!-- end widget -->
        </article>
        <!-- NEW WIDGET START -->

        <article class="col-xs-12 col-sm-12 col-md-12 col-lg-4">

            <!-- Widget ID (each widget will need unique ID)-->
            <div class="jarviswidget jarviswidget-color-write" id="wid-id-5" data-widget-editbutton="false" data-widget-colorbutton="false" data-widget-deletebutton="false">
                <!-- widget options:
                usage: <div class="jarviswidget" id="wid-id-0" data-widget-editbutton="false">
                -->
                <header>
                    <span class="widget-icon"> <i class="fa fa-table"></i> </span>
                    <h2>Data-uwb_loc</h2>

                </header>

                <!-- widget div-->
                <div>
                    <!-- widget content -->
                    <div class="widget-body">
                        <?php if ($data_uwb_loc){?>
                        <p>
                            field: <code>tag_id, pos_x, pos_y, pos_z, receiver, ts</code>
                        </p>
                        <p>
                            length: <code><?= count($data_uwb_loc)?></code>
                        </p>
                        <p>
                            ts: <code>
                                <?= $data_uwb_loc[0]->ts?>
                                - 
                                <?= end($data_uwb_loc)->ts?>
                            </code>
                        </p>
                        <p>
                            date: <code>
                                <?= date("Y-m-d H:i", $data_uwb_loc[0]->ts / 1000) ?>
                                -
                                <?= date("Y-m-d H:i", end($data_uwb_loc)->ts / 1000) ?>
                            </code>
						</p>
                        <hr class="simple">
                        <p>
                            api: <a href="<?= base_url()."/public/survey/api_data/survey_uwb_loc/".$event->event_id?>"><code>link</code></a>
                        </p>
                        <p>
                            csv: <a href="survey/download/survey_uwb_loc/<?=$event->event_id?>" class="btn btn-xs bg-color-blue txt-color-white">uwb_loc: <?= $event->event_id?></a>
                        </p>
                        <?php }else{?>
                            <p>No Data</p>
                        <?php }?>
                    </div>
                    <!-- end widget content -->
                    
                </div>
                <!-- end widget div -->

            </div>
            <!-- end widget -->
        </article>
        <!-- NEW WIDGET START -->
    </div>
</section>
<!-- end widget grid -->

<!-- <link rel="stylesheet" type="text/css" href="css/DataTables-1.10.22/css/dataTables.bootstrap.min.css"/> -->

<script type="text/javascript">
	// PAGE RELATED SCRIPTS

	loadScript("<?= base_url('public/js/plugin/datatables/datatables.min.js')?>", dt_2);

	function dt_2() {
		loadScript("<?= base_url('public/js/plugin/datatables/ColReorder-1.5.2/js/dataTables.colReorder.min.js')?>", dt_3);
	}

	function dt_3() {
		loadScript("<?= base_url('public/js/plugin/datatables/FixedColumns-3.3.1/js/dataTables.fixedColumns.min.js')?>", dt_4);
	}

	function dt_4() {
		loadScript("<?= base_url('public/js/plugin/datatables/dataTables.colVis.js')?>", dt_6);
	}

	// function dt_5() {
	// 	loadScript("<?= base_url('js/plugin/datatables/ZeroClipboard.js')?>", dt_6);
	// }

	function dt_6() {
		loadScript("<?= base_url('public/js/plugin/datatables/dataTables.tableTools.min.js')?>", dt_7);
	}

	function dt_7() {
		loadScript("<?= base_url('public/js/plugin/datatables/DataTables-1.10.22/js/dataTables.bootstrap4.min.js')?>", runDataTables);
	}

	function runDataTables() {

		/*
		 * BASIC
		 */

		$('#dt_basic').dataTable({

			// sPaginationType : "full_numbers",
			dom : "<'dt-row dt-top-row'lf><'dt-row'B><'clear'>r<'dt-wrapper't><'dt-row dt-bottom-row'ip>",
			order: [[0, "desc"]],
            buttons: [
                {
                    extend: 'csv',
                    text: 'Copy all data',
                    exportOptions: {
                        modifier: {
                            search: 'none'
                        }
                    }
                }
            ],
		});

		// $(document).ready(function() {
		// 	var table1 = $('#dt_basic').DataTable();
		// 	$("#dt_basic tbody").on("click","tr",function(){
		// 		var data = table1.row( this ).data();
		// 		alert(data[0]);
		// 	});
        // });

		/* END BASIC */
	}

</script>
<script type="text/javascript">
	// PAGE RELATED SCRIPTS
	$('#event-form').submit(function(e){
		$.post( "<?=base_url('survey/update')?>", $( "#event-form" ).serialize()).done(function(data) {
            if(data == '0'){
                alert('please fill required field.');
            }else{
                $('#done').html(data);
                setTimeout(function(){location.reload();}, 5000);
            }
		});
		return false;
	});
</script>