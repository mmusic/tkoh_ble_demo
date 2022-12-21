console.log("polygon.js");
mapboxgl.accessToken = '<?=$mapbox_key?>';
	var map = new mapboxgl.Map({
		container: 'map',
		style: 'mapbox://styles/mapbox/streets-v11',
		center: [114.21402, 22.3235],
		zoom: 19,
		bearing: 85
	});

	map.on('load', function() {
		map.addSource('national-park', {
			'type': 'geojson',
			'data': <?=$geojson?>
		});

		map.addLayer({
			'id': 'park-boundary',
			'type': 'line',
			'source': 'national-park',
			'layout': {
			'line-join': 'round',
			'line-cap': 'round'
			},
			'paint': {
			'line-color': '#BF93E4',
			'line-width': 2
			}
		});
	});						

	var draw = new MapboxDraw({
		displayControlsDefault: false,
		controls: {
			polygon: true,
			trash: true
		}
	});

	map.addControl(draw);

	draw.add({ type: 'Polygon', coordinates:  [[
		[114.21421654994128, 22.323443055138483],
		[114.2141174660099, 22.32320963054694],
		[114.21407880922527, 22.323517373549407],
		[114.21413148255846, 22.32364367905086],
		[114.21421654994128, 22.323443055138483]
		]] });

	map.on('draw.create', updateArea);
	map.on('draw.delete', updateArea);
	map.on('draw.update', updateArea);

	function updateArea(e) {
		var data = draw.getAll();
		var answer = document.getElementById('calculated-area');
		if (data.features.length > 0) {
			var area = turf.area(data);
			// restrict to area to 2 decimal points
			var rounded_area = Math.round(area * 100) / 100;
		} else {
			if (e.type !== 'draw.delete')
				alert('Use the draw tools to draw a polygon!');
		}
	}

	document.getElementById('export').onclick = function(e){
		// extract GeoJson from featureGroup
		var data = draw.getAll();

		if(data.features.length > 0){
			// Stringify the GeoJson
			var convertedData = 'text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data))

			// create export
			// document.getElementById('export').setAttribute('href', 'data:' + convertedData);
			// document.getElementById('export').setAttribute('download', 'data.geojson');
			// console.log(data);
			$.post( "<?=base_url('polygon/add/1001/1')?>", {data: data}).done(function(data) {
				// if(data == '0'){
					alert(data);
				// }else{
				// 	window.location.href="<?=base_url('survey/event').'/'?>" + data;
				// }
			});
		}
		else{
			alert("Wouldn't you like to draw some data")
		}
		}