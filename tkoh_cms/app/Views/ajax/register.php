<!-- widget grid -->
<section id="widget-grid" class="">

	<!-- row -->
	<div class="row">

		<!-- NEW WIDGET START -->
		<article class="col-xs-12 col-sm-12 col-md-12 col-lg-6">

			<!-- Widget ID (each widget will need unique ID)-->
			<div class="jarviswidget jarviswidget-color-blueDark"
				data-widget-editbutton="false"
				data-widget-colorbutton="false"
				data-widget-deletebutton="false"
				data-widget-togglebutton="false"
				data-widget-sortable="false"
				data-widget-fullscreenbutton="false">

				<header>
					<span class="widget-icon"> <i class="fa fa-table"></i> </span>
					<h2>Sensors</h2>

				</header>

				<!-- widget div-->
				<div>
					<!-- widget content -->
					<div class="widget-body no-padding">

						<div class="widget-body-toolbar"></div>
						<table id="datatable_register_record" class="table table-striped table-bordered table-hover">
							<thead>
								<tr>
									<th class="text-align-center">Sensor BLE Mac</th>
									<th class="text-align-center">Site</th>
                                    <th class="text-align-center">Label</th>
								</tr>
							</thead>
							<tbody>
								<?php foreach($sensors as $sensor_item) {?>
								<tr>
									<td class="text-align-center">
                                        <strong>
                                            <a href="<?=base_url('register/').'/'.$sensor_item['sensor']?>" style="cursor:pointer"><?= $sensor_item['sensor']?></a>
                                        </strong>
                                    </td>
                                    <td class="text-align-center">
                                        <strong>
                                            <?php foreach ($site_names as $site_name_item) {
                                                $site_name = '<div style="color:#F39C12">null</div>';
                                                if ($sensor_item['site'] == $site_name_item['site']) {
                                                    $site_name = $site_name_item['site_name'];
                                                    break;
                                                }
                                            } echo $site_name;?>
                                        </strong>
                                    </td>
                                    <td class="text-align-center"><?= $sensor_item['label']?> </td>
								</tr>
								<?php }?>
							</tbody>
						</table>
					</div>
					<!-- end widget content -->
                    
				</div>
				<!-- end widget div -->

			</div>
			<!-- end widget -->
        </artivle>
        
    </div>
</section>
<!-- end widget grid -->

<script type="text/javascript">

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

    function dt_6() {
        loadScript("<?= base_url('public/js/plugin/datatables/dataTables.tableTools.min.js')?>", dt_7);
    }

    function dt_7() {
        loadScript("<?= base_url('public/js/plugin/datatables/DataTables-1.10.22/js/dataTables.bootstrap4.min.js')?>", runDataTables);
    }

	function runDataTables() {

		$('#datatable_register_record').dataTable({
			sPaginationType : "full_numbers",
			dom : "<'dt-row dt-top-row'lf><'dt-row'B><'clear'>r<'dt-wrapper't><'dt-row dt-bottom-row'ip>",
			order: [[0, "desc"]],
			buttons: [
				{
					className: 'btn btn-primary btn-primary-sm',
					text: 'New Sensor',
					action: function ( e, dt, node, config ) {
						window.location.href="<?=base_url('register/sensor')?>";
					}
				}
			]
        });
        

		// $(document).ready(function() {
		// 	var table1 = $('#dt_basic').DataTable();
		// 	$("#dt_basic tbody").on("click","tr th",function(){
		// 		var data = table1.row( this ).data();
		// 		window.location.href="survey?id=" + data[0];
		// 	});
        // });

		/* END BASIC */
	}

</script>
