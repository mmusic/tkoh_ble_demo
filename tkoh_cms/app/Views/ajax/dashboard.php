<!-- widget grid -->
<section id="widget-grid" class="">

	<!-- row -->
	<div class="row">

		<article class="col-sm-12 col-md-12 col-lg-6">
		<!-- new widget -->
			<div class="jarviswidget jarviswidget-color-blueDark" id="wid-id-1"
				data-widget-editbutton="false"
				data-widget-colorbutton="false"
				data-widget-deletebutton="false"
				data-widget-togglebutton="false"
				data-widget-sortable="false">

				<!-- widget options:
				data-widget-colorbutton="false"
				data-widget-editbutton="false"
				data-widget-togglebutton="false"
				data-widget-deletebutton="false"
				data-widget-fullscreenbutton="false"
				data-widget-custombutton="false"
				data-widget-collapsed="true"
				data-widget-sortable="false"
				-->

				<header>
					<span class="widget-icon"> <i class="fa fa-map-marker"></i> </span>
					<h2>Sensor</h2>
				</header>

				<!-- widget div-->
				<div>

					<div class="widget-body no-padding">
						<!-- content goes here -->
						<table id="datatable_sensor" class="table table-striped table-hover">
							<thead>
								<tr>
									<th class="text-align-center" width='15%'>Site</th>
									<th class="text-align-center" width='5%'>Label</th>
									<th class="text-align-center" width='30%'>Sensor</th>
									<th class="text-align-center" width='35%'>HCI</th>
									<th class="text-align-center" width='15%'>VM</th>
								</tr>
							</thead>
							<tbody id='statusbody'>
							</tbody>
						</table>
						<!-- end content -->
					</div>
				</div>
				<!-- end widget div -->
			</div>
			<!-- end widget -->

			<!-- new widget -->
			<div class="jarviswidget jarviswidget-color-blueDark" id="wid-id-2" data-widget-colorbutton="false" 
				data-widget-editbutton="false"
				data-widget-colorbutton="false"
				data-widget-deletebutton="false"
				data-widget-togglebutton="false"
				data-widget-sortable="false">

				<header>
					<span class="widget-icon"> <i class="fa fa-map-marker"></i> </span>
					<h2>Logger</h2>
				</header>

				<!-- widget div-->
				<div>
					<div class="widget-body no-padding">
						<!-- content goes here -->
						<table id="datatable_logger" class="table table-bordered smart-form">
							<thead>
								<tr>
									<th class="text-align-center"> <i class="fa fa-building"></i> Date</th>
									<th class="text-align-center"> <i class="fa fa-calendar"></i> S-Type</th>
									<th class="text-align-center"> <i class="glyphicon glyphicon-send"></i> Content</th>
									<th class="text-align-center"> <i class="glyphicon glyphicon-send"></i> Sloved</th>
								</tr>
								<tr class="second">
									<td>
										<label class="input">
											<input type="text" name="search_date" placeholder="Filter time" class="search_init">
										</label>
									</td>
									<td>
										<label class="input">
											<input type="text" name="search_src_type" placeholder="Filter source type" class="search_init">
										</label>	
									</td>
									<td>
										<label class="input">
											<input type="text" name="search_content" placeholder="Filter content" class="search_init">
										</label>	
									</td>
									<td>
										<label class="input">
											<input type="text" name="search_content" placeholder="Filter content" class="search_init">
										</label>	
									</td>
								</tr>
							</thead>
							<tbody>
								<?php foreach($logs as $logs_item){ ?>
									<tr class= "<?= $log_level_mapping[$logs_item['level']]?>">
										<td class="text-align-center"><?= date('Y/m/d H:i:s', $logs_item['ts']/1000)?></td>
										<td class="text-align-center"><code><?= $logs_item['src_type']?></code></td>
										<td class="text-align-center"><?= $logs_item['content']?></td>
										<td class="text-align-center"><?php if ($logs_item['todo']){echo '<i class="fa fa-check-circle">';}?></td>
									</tr>
								<?php } ?>
							</tbody>
						</table>

						<!-- end content -->
					</div>
				</div>
				<!-- end widget div -->
			</div>
			<!-- end widget -->

		</article>

		<article class="col-sm-12 col-md-12 col-lg-6">

			<!-- new widget -->
			<div class="jarviswidget jarviswidget-color-blueDark" id="wid-id-3" 
				data-widget-editbutton="false"
				data-widget-colorbutton="false"
				data-widget-deletebutton="false"
				data-widget-togglebutton="false"
				data-widget-sortable="false">

				<header>
					<span class="widget-icon"> <i class="fa fa-calendar"></i> </span>
					<h2> Reporting </h2>
					<div class="widget-toolbar">
						<!-- add: non-hidden - to disable auto hide -->
						<div class="btn-group">
							<button class="btn dropdown-toggle btn-xs btn-default" data-toggle="dropdown">
								Showing <i class="fa fa-caret-down"></i>
							</button>
							<ul class="dropdown-menu js-status-update pull-right">
								<li>
									<a href="javascript:void(0);" id="mt">Month</a>
								</li>
								<li>
									<a href="javascript:void(0);" id="ag">Agenda</a>
								</li>
								<li>
									<a href="javascript:void(0);" id="td">Today</a>
								</li>
							</ul>
						</div>
					</div>
				</header>

				<!-- widget div-->
				<div>
					<!-- widget edit box -->
					<div class="jarviswidget-editbox">

						<input class="form-control" type="text">

					</div>
					<!-- end widget edit box -->

					<div class="widget-body no-padding">
						<!-- content goes here -->
						<div class="widget-body-toolbar">

							<div id="calendar-buttons">

								<div class="btn-group">
									<a href="javascript:void(0)" class="btn btn-default btn-xs" id="btn-prev"><i class="fa fa-chevron-left"></i></a>
									<a href="javascript:void(0)" class="btn btn-default btn-xs" id="btn-next"><i class="fa fa-chevron-right"></i></a>
								</div>
							</div>
						</div>
						<div id="calendar"></div>

						<!-- end content -->
					</div>

				</div>
				<!-- end widget div -->
			</div>
			<!-- end widget -->
		</article>
	</div>
	<!-- end row -->

</section>
<!-- end widget grid -->

<script type="text/javascript">
	
	/*
	 * FULL CALENDAR JS
	 */
	
	// Load Calendar dependency then setup calendar
	loadScript("public/js/plugin/fullcalendar/jquery.fullcalendar.min.js", setupCalendar);
	
	function setupCalendar() {
	
	    if ($("#calendar").length) {
	        var date = new Date();
	        var d = date.getDate();
	        var m = date.getMonth();
	        var y = date.getFullYear();
	        var calendar = $('#calendar').fullCalendar({

	            selectable: false,
	            unselectAuto: false,
	            disableResizing: false,
	
	            header: {
	                left: 'title', //,today
	                center: 'prev, next, today',
	                right: 'month, agendaWeek, agenDay' //month, agendaDay,
				},
				
				eventClick: function (arg) {
					// window.location.href = arg.title;
					// window.location.href = 'maintenance';
					// console.log(arg);
				},

	            eventRender: function (event, element, icon) {
	                if (!event.description == "") {
	                    element.find('.fc-event-title').append("<br/><span class='ultra-light'>" + event.description +
	                        "</span>");
	                }
	                if (!event.icon == "") {
	                    element.find('.fc-event-title').append("<i class='air air-top-right fa " + event.icon +
	                        " '></i>");
	                }
				},
				events: [<?php foreach($todos as $todo){echo json_encode($todo).',';}; foreach($reports as $report){echo json_encode($report).',';};?>],
	        });
	
	    };
	
	    /* hide default buttons */
	    $('.fc-header-right, .fc-header-center').hide();
	}

	// calendar prev
	$('#calendar-buttons #btn-prev').click(function () {
	    $('.fc-button-prev').click();
	    return false;
	});
	
	// calendar next
	$('#calendar-buttons #btn-next').click(function () {
	    $('.fc-button-next').click();
	    return false;
	});
	
	// calendar today
	$('#calendar-buttons #btn-today').click(function () {
	    $('.fc-button-today').click();
	    return false;
	});
	
	// sampling
	// calendar month
	$('#mt').click(function () {
		$('#calendar').fullCalendar('changeView', 'month');
	});
	
	// calendar agenda week
	$('#ag').click(function () {
	    $('#calendar').fullCalendar('changeView', 'agendaWeek');
	});
	
	// calendar agenda day
	$('#td').click(function () {
	    $('#calendar').fullCalendar('changeView', 'agendaDay');
	});

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

		/* END BASIC */

		/* Add the events etc before DataTables hides a column */
		$("#datatable_logger thead input").keyup(function() {
			oTable.fnFilter(this.value, oTable.oApi._fnVisibleToColumnIndex(oTable.fnSettings(), $("thead input").index(this)));
		});

		$("#datatable_logger thead input").each(function(i) {
			this.initVal = this.value;
		});
		$("#datatable_logger thead input").focus(function() {
			if (this.className == "search_init") {
				this.className = "";
				this.value = "";
			}
		});
		$("#datatable_logger thead input").blur(function(i) {
			if (this.value == "") {
				this.className = "search_init";
				this.value = this.initVal;
			}
		});		

		var oTable = $('#datatable_logger').dataTable({
			dom : "<'dt-top-row'><'dt-wrapper't><'dt-row dt-bottom-row'ip>",
			//"sDom" : "t<'row dt-wrapper'<'col-sm-6'i><'dt-row dt-bottom-row'<'row'<'col-sm-6'i><'col-sm-6 text-right'>>",
			"oLanguage" : {
				"sSearch" : "Search all columns:"
			},
			"bSortCellsTop" : true,
			order: [[0, "desc"]],
		});

		var oTable = $('#datatable_sensor').dataTable({
			dom : "<'dt-top-row'><'dt-wrapper't><'dt-row dt-bottom-row'ip>",
			//"sDom" : "t<'row dt-wrapper'<'col-sm-6'i><'dt-row dt-bottom-row'<'row'<'col-sm-6'i><'col-sm-6 text-right'>>",
			"oLanguage" : {
				"sSearch" : "Search all columns:"
			},
			"bSortCellsTop" : true,
			order: [[0, "desc"]],
		});
		/* END TABLE TOOLS */
	}

	load_sensor_status();
	function load_sensor_status() {
		$.get("monitor/get_sensor_status_dashboard", '', function(result){
			// data = JSON.parse(result);
			// console.log(result);
			$('#statusbody').html(result).delay(100);
			setTimeout(load_sensor_status, 1000);
		});
		// $.ajax({
		// 	type: "GET",
		// 	url: "dashboard/real_time_sensor_status",
		// 	dataType: 'html',
		// 	cache: true, // (warning: this will cause a timestamp and will call the request twice)
		// 	beforeSend: function () {
		// 		// container.html('<h1><i class="fa fa-cog fa-spin"></i> Loading...</h1>');
		// 	},
		// 	success: function (data) {
		// 		// console.log("load_sensor_status");
		// 		$('#statusbody')
		// 			.html(data)
		// 			.delay(100);
		// 		setTimeout(load_sensor_status, 1000);
		// 	},
		// 	error: function (xhr, ajaxOptions, thrownError) {
		// 		// container.html(
		// 		// 	'<h4 style="margin-top:10px; display:block; text-align:left"><i class="fa fa-warning txt-color-orangeDark"></i> Error 404! Page not found.</h4>'
		// 		// );
		// 	},
		// 	async: false
		// });
	}

</script>