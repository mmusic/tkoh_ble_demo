			</div>
			<!-- END MAIN CONTENT -->				
		</div>
		<!-- END MAIN PANEL -->
	</body>	
</html>

<script>
	pageSetUp();
	get_time();
	function get_time() {
		$.get("<?=base_url('dashboard/get_time')?>").done(function(data) {
			$('#time').html(data);
			setTimeout(get_time, 1000);
		});
	}

	// loadOSStatus();
	// function loadOSStatus() {
	// 	$.getJSON("<?=base_url('sysinfo/get_os_status')?>").done(function(data) {
	// 		$('#time').html(data);
	// 		$('#cpu').html(data['cpu'] + "%");
	// 		$('#memory').html(data['memory']['usage'] + "%");
	// 		$('#storage').html(data['storage'] + "%");
	// 		// setTimeout(loadOSStatus, 5000);
	// 	})
	// }
</script>