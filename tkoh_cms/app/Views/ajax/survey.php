<!-- widget grid -->
<section id="widget-grid" class="">

	<!-- row -->
	<div class="row">

		<!-- NEW WIDGET START -->
		<article class="col-xs-12 col-sm-12 col-md-12 col-lg-12">

			<!-- Widget ID (each widget will need unique ID)-->
			<div class="jarviswidget jarviswidget-color-darken" id="wid-id-0"
				data-widget-editbutton="false"
				data-widget-colorbutton="false"
				data-widget-deletebutton="false"
				data-widget-togglebutton="false"
				data-widget-sortable="false"
				data-widget-fullscreenbutton="false">

				<header>
					<span class="widget-icon"> <i class="fa fa-table"></i> </span>
					<h2>Survey Events </h2>

				</header>

				<!-- widget div-->
				<div>
					<!-- widget content -->
					<div class="widget-body no-padding">

						<div class="widget-body-toolbar">
                        </div>
						<table id="dt_basic" class="table table-striped table-bordered table-hover">
							<thead>
								<tr>
									<th>Event_ID</th>
									<th>Date</th>
									<th>Site</th>
									<th>Remark</th>
								</tr>
							</thead>
							<tbody>
								<?php foreach($event_all as $event_item) {?>
								<tr>
									<td><strong><a href="<?=base_url('survey/event').'/'.$event_item->event?>" style="cursor:pointer"><?= $event_item->event?></a></strong></td>
									<td><?= $event_item->date?></td>
									<td><?= $event_item->site?> </td>
								<td><?php if($event_item->remark){?><i class="fa fa-check fa-fw "><?php }?></td>
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

<link rel="stylesheet" type="text/css" href="<?=base_url('public/css/DataTables-1.10.22/css/dataTables.bootstrap.min.css')?>"/>

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

		$('#dt_basic').dataTable({

			sPaginationType : "full_numbers",
			dom : "<'dt-row dt-top-row'lf><'dt-row'B><'clear'>r<'dt-wrapper't><'dt-row dt-bottom-row'ip>",
			order: [[0, "desc"]],
			buttons: [
				{
					className: 'btn btn-primary btn-primary-sm',
					text: 'New Event',
					action: function ( e, dt, node, config ) {
						window.location.href="<?=base_url('survey/new_event')?>";
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
