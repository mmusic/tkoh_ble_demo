<script src="<?= base_url('/public/js/mapbox/turf.min.js')?>"></script>
<script src="<?= base_url('/public/js/mapbox/mapbox-gl-draw.js')?>"></script>
<link href="<?= base_url('/public/css/mapbox/mapbox-gl-draw.css')?>" rel="stylesheet" />
<style>
    /* style for switching floor */
    #menu {
        background: #fff;
        position: absolute;
        z-index: 1;
        top: 10px;
        right: 50px;
        border-radius: 3px;
        width: 120px;
        border: 1px solid rgba(0, 0, 0, 0.4);
        font-family: 'Open Sans', sans-serif;
    }
    
    #menu a {
        font-size: 13px;
        color: #404040;
        display: block;
        margin: 0;
        padding: 0;
        padding: 10px;
        text-decoration: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.25);
        text-align: center;
    }
    
    #menu a:last-child {
        border: none;
    }
    
    #menu a:hover {
        background-color: #f8f8f8;
        color: #404040;
    }
    
    #menu a.active {
        background-color: #3887be;
        color: #ffffff;
    }
    
    #menu a.active:hover {
        background: #3074a4;
    }
</style>
<!-- widget grid -->
<section id="widget-grid" class="">
	<!-- row -->
	<div class="row">
		<article class="col-sm-12 col-md-12 col-lg-12">
			<!-- Widget ID (each widget will need unique ID)-->
			<div class="jarviswidget jarviswidget-color-darken" id="wid-id-0" 
				data-widget-editbutton="false"
				data-widget-colorbutton="false"
				data-widget-deletebutton="false"
				data-widget-togglebutton="false"
				data-widget-sortable="false">

				<header>
					<span class="widget-icon"> <i class="fa fa-map-marker"></i> </span>
					<h2>Polygon</h2>
				</header>

				<!-- widget div-->
				<div>
					<!-- widget content -->
					<div class="widget-body">
						<?php foreach($site_names as $site_name) {?>
						<a href="<?= base_url('polygon/'.$site_name['site_name'])?>" class="btn btn-success"><?= $site_name['site_name']?></a>
						<?php } ?>
						<hr class="simple">
						<div class="row no-space">
							<div class="col-xs-12 col-sm-12 col-md-8 col-lg-9" style="height:730px;">
								<!-- TODO: MAP -->
								<nav id="menu"></nav>
								<div id="map"></div>
							</div>
							<div class="col-xs-12 col-sm-12 col-md-4 col-lg-3"> 
								<div class="calculation-box">
									<button type="submit" id="save_polygon" class="btn btn-primary">Save Polygon & Source</button>
									<!-- <button type="submit" id="export_polygon" class="btn btn-success">Export</button> -->
								</div>
								<hr class="simple">
								<!-- <form id="import-form" class="smart-form">
									<fieldset>
										<div class="row">
											<section class="col col-9">
												<label class="input state-success" >
													<input type="text" name="import"></input>
												</label>
											</section>
											<section class="col col-3">
												<button type="submit" class="btn btn-primary btn-sm">Import</button>
											</section>
										</div>
									</fieldset>
								</form> -->
								<!-- <hr class="simple"> -->
								<header>HISTORY</header>
								<table id="datatable_tscreate" class="table table-striped table-bordered table-hover">
									<thead>
										<tr>
											<th class="text-align-center">Polygons <?= $site_info[0]['site_name']?></th>
											<th class="text-align-center"></th>
										</tr>
									</thead>
									<tbody id='ts_create_content'>
									</tbody>
								</table>

								<form id="updatesource-form" class="smart-form">
    								<header>Update Source</header>
    									<section class="col-xs-12 col-sm-12 col-md-12 col-lg-6">
    										<label class="Label">S_idx</label>
    										<label class="input"> <i class="icon-prepend fa fa-barcode"></i>
    											<input name="idx" onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}">
    										</label>
    									</section>
    									<section class="col-xs-12 col-sm-12 col-md-12 col-lg-6">
    										<label class="Label">S_name</label>
    										<label class="input"> <i class="icon-prepend fa fa-text-width"></i>
    											<input name="name">
    										</label>
    									</section>

    								<footer>
    									<button type="submit" class="btn btn-primary">Update to <?= $sub_title?></button>
    								</footer>
    							</form>
							</div>
						</div>
					</div>
					<!-- end widget content -->				
				</div>
				<!-- end widget div -->
			</div>
			<!-- end widget -->
		</article>
    </div>
</section>

<!-- end widget grid -->
<script>
	loadDataTableScripts();
	function loadDataTableScripts() {

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
	}

	function runDataTables() {

		var table = $('#datatable_tscreate').dataTable({
			sPaginationType : "full_numbers",
			dom : "<'dt-row dt-top-row'><'clear'>r<'dt-wrapper't><'dt-row dt-bottom-row'ip>",
			order: [[0, "desc"]],
		});
	}
</script>

<?php if ($site_info){?>
<script>
	mapboxgl.accessToken = '<?=$mapbox_key?>';
	var dot_mapping = <?= $site_info[0]['dot_mapping']?>;
	var floor_cur = <?php if($site_polygons){echo $site_polygons[0]->floor;}else{echo $site_info[0]['floor'];} ?>;

	var map = new mapboxgl.Map({
		container: 'map',
        style: 'mapbox://styles/mapbox/light-v10',
        center: [<?= $site_info[0]['mapbox_center_lng']?>, <?= $site_info[0]['mapbox_center_lat']?>],   
        zoom: <?= $site_info[0]['mapbox_zoom']?>,
        bearing: <?= $site_info[0]['mapbox_bearing']?> 
	});

	var site_map_geojson;
	<?php foreach ($site_info as $site_info_item) { ?>
		if (<?= $site_info_item['floor']?> == floor_cur) {
			site_map_geojson = <?= $site_info_item['geojson']?>;
		}
	<?php } ?>
	
	map.on('load', function() {
		map.addSource('site_map', {
			'type': 'geojson',
			'data': site_map_geojson
		});

		// Source: source list
        map.addSource('source_list', {
            'type': 'geojson',
            'data': {
                "type": "FeatureCollection",
                "features": []
            }
        });

		// Source: site draw ploygons with ts_create
		map.addSource('polygons', {
			'type': 'geojson',
			'data': {
				'type': 'FeatureCollection',
				'features': []
			}
		});

		// Source: site draw ploygons with ts_create
		map.addSource('polygons_idx', {
			'type': 'geojson',
			'data': {
				'type': 'FeatureCollection',
				'features': []
			}
		});
		
		// Layer: site fix ploygons with ts_create
		map.addLayer({
			'id': 'polygons_layer',
			'type': 'fill',
			'source': 'polygons',
			'layout': {
                'visibility': 'visible'
			},
			'paint': {
				'fill-color': '#58D68D',
				'fill-opacity': 0.2
			}
		});

		// Layer: site fix ploygons idx with ts_create
		map.addLayer({
            'id': 'polygon_idx_layer',
            'type': 'symbol',
            'source': 'polygons_idx',
            'layout': {
				'text-field': ['get', 'polygon_idx'],
				'text-size': 20,
                'visibility': 'visible',
            },
			'paint': {
                'text-color': '#21618C',
            },
            // 'filter': ['==', '$type', 'Point']
        });

		// Layer: beacon dots
        map.addLayer({
            'id': 'source_list_layer',
            'type': 'circle',
            'source': 'source_list',
            'paint': {
                'circle-radius': 6,
                'circle-color': ['get', 'color']
            },
            'layout': {
                'visibility': 'visible'
            },
            // 'filter': ['==', '$type', 'Point']
        });

		// Layer: source info (name & coor)
        map.addLayer({
            'id': 'source_info_layer',
            'type': 'symbol',
            'source': 'source_list',
            'layout': {
                "text-field": ["format", ["get", "source_idx"], {
                    "text-color": '#424949',
                },
                "\n", {},
                ["get", "source_name"], {
                    "text-color": '#F39C12',
                },
                "\n", {}],
                'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                'text-size': 20,
                'text-offset': [0, 0.3],
                'text-anchor': 'top',  
                'visibility': 'visible'
            }
        });

		map.addLayer({
            'id': 'site_map_layer',
            'type': 'line',
            'source': 'site_map',
            'layout': {
                'line-join': 'round',
                'line-cap': 'round'
            },
            'paint': {
                'line-color': '#BB8FCE',
                'line-width': 2
            }
        });

		draw_point_and_polygons();
	});

	function latlng2xy(lng, lat){
        // floor_cur
		var pixel_mapbox = map.project([lng, lat]);
        var mA = {x: dot_mapping[0]['x'], y: dot_mapping[0]['y']};
        var mB = {x: dot_mapping[1]['x'], y: dot_mapping[1]['y']};
        var pA = map.project([dot_mapping[0]['lng'], dot_mapping[0]['lat']]);
        var pB = map.project([dot_mapping[1]['lng'], dot_mapping[1]['lat']]);

		x = (pixel_mapbox.x - pA.x) * (mB.x - mA.x) / (pB.x - pA.x) + mA.x;
		y = (pixel_mapbox.y - pA.y) * (mB.y - mA.y) / (pB.y - pA.y) + mA.y;

		return [x, y]
	}

	function xy2latlng(x, y){
        var mA = {x: dot_mapping[0]['x'], y: dot_mapping[0]['y']};
        var mB = {x: dot_mapping[1]['x'], y: dot_mapping[1]['y']};
        var pA = map.project([dot_mapping[0]['lng'], dot_mapping[0]['lat']]);
        var pB = map.project([dot_mapping[1]['lng'], dot_mapping[1]['lat']]);

        var cx = (x - mA.x) * (pB.x - pA.x) / (mB.x - mA.x) + pA.x;
        var cy = (y - mA.y) * (pB.y - pA.y) / (mB.y - mA.y) + pA.y;

        return map.unproject([cx, cy]);
    }

	var draw = new MapboxDraw({
		displayControlsDefault: false,
		controls: {
			point: true,
			// line_string: true,
			polygon: true,
			trash: true
		},
		// reference： https://github.com/mapbox/mapbox-gl-draw/blob/main/docs/EXAMPLES.md
		styles: [
			// points
			{
				'id': 'highlight-active-points',
				'type': 'circle',
				'filter': ['all',
					['==', '$type', 'Point'],
					['==', 'meta', 'feature'],
					['==', 'active', 'true']],
				'paint': {
					'circle-radius': 10,
					'circle-color': '#27AE60'
				}
				},
				{
				'id': 'points-are-blue',
				'type': 'circle',
				'filter': ['all',
					['==', '$type', 'Point'],
					['==', 'meta', 'feature'],
					['==', 'active', 'false']],
				'paint': {
					'circle-radius': 8,
					'circle-color': '#2980B9'
				}
			},

			// polygons
			{
                'id': 'gl-draw-polygon-fill-inactive',
                'type': 'fill',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Polygon'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'fill-color': '#3bb2d0',
                    'fill-outline-color': '#3bb2d0',
                    'fill-opacity': 0.1
                }
            },
            {
                'id': 'gl-draw-polygon-fill-active',
                'type': 'fill',
                'filter': ['all', ['==', 'active', 'true'],
                    ['==', '$type', 'Polygon']
                ],
                'paint': {
                    'fill-color': '#fbb03b',
                    'fill-outline-color': '#fbb03b',
                    'fill-opacity': 0.1
                }
            },
            {
                'id': 'gl-draw-polygon-midpoint',
                'type': 'circle',
                'filter': ['all', ['==', '$type', 'Point'],
                    ['==', 'meta', 'midpoint']
                ],
                'paint': {
                    'circle-radius': 3,
                    'circle-color': '#fbb03b'
                }
            },
            {
                'id': 'gl-draw-polygon-stroke-inactive',
                'type': 'line',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Polygon'],
                    ['!=', 'mode', 'static']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#3bb2d0',
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-polygon-stroke-active',
                'type': 'line',
                'filter': ['all', ['==', 'active', 'true'],
                    ['==', '$type', 'Polygon']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#fbb03b',
                    'line-dasharray': [0.2, 2],
                    'line-width': 2
                }
            },
			{
                'id': 'gl-draw-line-inactive',
                'type': 'line',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'LineString'],
                    ['!=', 'mode', 'static']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#3bb2d0',
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-line-active',
                'type': 'line',
                'filter': ['all', ['==', '$type', 'LineString'],
                    ['==', 'active', 'true']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#fbb03b',
                    'line-dasharray': [0.2, 2],
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-polygon-and-line-vertex-stroke-inactive',
                'type': 'circle',
                'filter': ['all', ['==', 'meta', 'vertex'],
                    ['==', '$type', 'Point'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-color': '#fff'
                }
            },
            {
                'id': 'gl-draw-polygon-and-line-vertex-inactive',
                'type': 'circle',
                'filter': ['all', ['==', 'meta', 'vertex'],
                    ['==', '$type', 'Point'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 3,
                    'circle-color': '#fbb03b'
                }
            },
		]
	});

	map.addControl(draw);
	
	// map.on('draw.create', updateArea);
	// map.on('draw.delete', updateArea);
	// map.on('draw.update', updateArea);

	// function updateArea(e) {
	// 	var data = draw.getAll();
	// }
	function draw_point_and_polygons(){
		// draw.deleteAll
		<?php if($site_polygons){ ?>
			var polygon_list = {};
			polygon_list['type'] = 'FeatureCollection';
			polygon_list['features'] = new Array;

			var polygon_idx_list = {};
			polygon_idx_list['type'] = 'FeatureCollection';
			polygon_idx_list['features'] = new Array;   

			<?php 
				foreach($site_polygons as $site_polygon_item){?>
					if (<?= $site_polygon_item->floor ?> == floor_cur) {
						draw.add({
							type: 'Polygon', 
							coordinates:  <?=$site_polygon_item->geojson?>,
							});

						var polygon_poly = {
							"type": "Feature",
							"geometry": {
								"type": "Polygon",
								"coordinates": <?=$site_polygon_item->geojson?>
							}
						};

						coors = <?= $site_polygon_item->geojson?>;
						avg_lng = 0;
						avg_lat = 0;
						for (i=0; i < 4; i++) {
							avg_lng = avg_lng + coors[0][i][0];
							avg_lat = avg_lat + coors[0][i][1];
							}
						// show polygon id
						var polygon_idx = {
							"type": "Feature",
							"geometry": {
								"type": "Point",
								"coordinates": [avg_lng/4, avg_lat/4]
							},
							"properties": {    
								'polygon_idx': '#<?=$site_polygon_item->poly?>',
							},
						};
						polygon_idx_list['features'].push(polygon_idx);

						polygon_list['features'].push(polygon_poly);
					}
			<?php }?>
			map.getSource('polygons').setData(polygon_list);
			map.getSource('polygons_idx').setData(polygon_idx_list);
		<?php }?>
		
		<?php if ($site_sources) { ?>
			var source_list = {};
			source_list['type'] = 'FeatureCollection';
			source_list['features'] = new Array;
			<?php
				foreach($site_sources as $source_item){ ?>
					if (<?= $source_item->floor ?> == floor_cur) {
						<?php if ($source_item->name) { 
							$source_name = $source_item->name;
						}else{
							$source_name = 'null';
						}?>
						
						draw.add({
							"type": "Feature",
								"properties": {    
									'source_idx': <?= $source_item->idx?>,
									'source_name': '<?= $source_name?>',
									'color': '#85C1E9',
								},
								"geometry": {
									"type": "Point",
									"coordinates": [<?= $source_item->lng?>, <?= $source_item->lat?>]
								}
							});

						var source_dot = {
								"type": "Feature",
								"properties": {    
									'source_idx': <?= $source_item->idx?>,
									'source_name': '<?= $source_name?>',
									'color': '#85C1E9',
								},
								"geometry": {
									"type": "Point",
									"coordinates": [<?= $source_item->lng?>, <?= $source_item->lat?>]
								}
						};
						source_list['features'].push(source_dot);
					}
			<?php }?>
			map.getSource('source_list').setData(source_list);
		<?php }?>
	}


	function get_floor_ts_create() {
		var ts_create_floor = '';
		<?php foreach ($site_ts_create as $key=>$site_ts_create_item) {?>
			if (<?= $site_ts_create_item->floor ?> == floor_cur) {
				ts_create_floor += '<tr><td class="text-align-center">';
				ts_create_floor += '<a href="<?= base_url('polygon/'.$site_info[0]['site_name'].'/'.$site_ts_create_item->ts_create)?>"><strong><?= date('m/d H:i', $site_ts_create_item->ts_create)?></strong></a>';
				ts_create_floor += '<?php if ($key == 0) {?>&nbsp&nbsp<span class="label label-warning">New!</span><?php }?></td>';
				ts_create_floor += '<td class="text-align-center">';
				ts_create_floor += '<a href="<?= base_url('polygon/export_geojson/'.$site_info[0]['site'].'/'.$site_ts_create_item->ts_create)?>"><i class="fa fa-download">G</i></a>&nbsp';
				ts_create_floor += '<a href="<?= base_url('polygon/export_meter/'.$site_info[0]['site'].'/'.$site_ts_create_item->ts_create)?>"><i class="fa fa-download">M</i></a>&nbsp';
				ts_create_floor += '<a href="<?= base_url('polygon/del/'.$site_info[0]['site'].'/'.$site_ts_create_item->ts_create)?>"><i class="fa fa-trash-o"></i></a></td></tr>';
					
			}
		<?php } ?>
		return ts_create_floor;
	}
	$('#ts_create_content').html(get_floor_ts_create());

	// floor switcher
	<?php foreach ($site_info as $idx => $site_floor_item) { ?>
            
		var link = document.createElement('a');
		link.href = '#';
		if (<?= $site_floor_item['floor'] ?> == floor_cur) {
			link.className = 'active';
		}
		link.textContent = '<?= $site_floor_item['floor_name']?>';
		
		link.onclick = function (e) {
			e.preventDefault();
			e.stopPropagation();
			$('a').removeClass('active');
			this.className = 'active';
			if (<?= $site_floor_item['floor'] ?> == floor_cur) {
				draw.deleteAll().getAll();
			}
			// check floor cur
			floor_cur = <?= $site_floor_item['floor']?>;
			dot_mapping = <?= $site_info[$site_floor_item['floor'] - 1]['dot_mapping']?>;
			draw_point_and_polygons();
			// set data
			map.getSource('site_map').setData(<?= $site_floor_item['geojson']?>);
			$('#ts_create_content').html(get_floor_ts_create());
		};
		document.getElementById('menu').appendChild(link);
	<?php } ?>

	$('#save_polygon').click(function(){
		// extract GeoJson from featureGroup
		var data = draw.getAll();
		console.log(data);
		if(data.features.length > 0){
			// for(var i = 0; i < data['features'].length; i++){
			// 	data['features'][i]['geometry']['xy'] = [[]];
			// 	data['features'][i]['geometry']['coordinates'][0].forEach(lnglat => {
			// 		data['features'][i]['geometry']['xy'][0].push(latlng2xy(lnglat[0], lnglat[1]));
			// 	});
			// }

			$.post( "<?=base_url('polygon/save/'.$site_info[0]['site'])?>/" + floor_cur, {raw_polygons: data}).done(function(data) {
				link = "<?= base_url('polygon/'.$site_info[0]['site_name'])?>" + "/" + data;
				window.location.href= link;
			});
		}
		else{
			alert("Wouldn't you like to draw some data");
		}
	});

	$('#import-form').submit(function(e){
		$.post("<?=base_url('polygon/import/'.$site_item->site.'/'.$site_item->floor)?>", $("#import-form").serialize()).done(function(data) {
            if(data == '0'){
                alert('error format, please fill again.');
			}else{
				link = "<?= base_url('polygon/'.$site_item->site.'/'.$site_item->floor)?>" + "/" + data;
				window.location.href= link;
            }
		});
		return false;
	});

	$('#updatesource-form').submit(function(e){
		$.post("<?=base_url('polygon/update_source/'.$ts_create)?>", $( "#updatesource-form" ).serialize()).done(function(data) {
            if(data == '0'){
                alert('please fill ');
            }else{
                link = "<?= base_url('polygon/'.$site_info[0]['site_name'])?>" + "/" + data;
				window.location.href= link;
            }
		});
		return false;
	});
</script>
<?php } ?>