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
					<h2>Register</h2>

				</header>

				<!-- widget div-->
				<div>
					<div class="widget-body no-padding">
						<form id="updatesensor-form" class="smart-form">
							<header>New Sensor Form</header>
							<fieldset>
                                <section>
                                    <label class="label">Sensor BLE Mac</label>
                                    <label class="input state-success"> <i class="icon-prepend fa fa-barcode"></i>
                                        <input type="text" name="sensor" value="<?= $sensor_info['sensor'] ?>" readonly="readonly">
                                    </label>
                                </section>
                                <section>
									<label class="label">Site</label>
                                    <label class="select">
                                        <select name="site">
                                        <option value=<?= $sensor_info['site'] ?> selected="selected" >
                                            <?php foreach ($site_names as $site_name_item) {
                                                if ($sensor_info['site'] == $site_name_item['site']) {
                                                    echo $site_name_item['site_name'];
                                                    break;
                                                }
                                            }?>
                                        </option>
                                            <?php foreach ($site_names as $site_name_item) {
                                                echo "<option value=\"".$site_name_item['site']."\">".$site_name_item['site_name']."</option>";
                                            } ?>
                                        </select> <i></i> </label>
                                </section>
                                <section class="col-xs-12 col-sm-12 col-md-12 col-lg-6">
                                    <label class="Label">Label</label>
                                    <label class="input"> <i class="icon-prepend fa  fa-calendar"></i>
                                        <input value="<?= $sensor_info['label'] ?>" name="label" onkeyup="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" onafterpaste="if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}">
                                    </label>
                                </section>
							</fieldset>

							<footer>
								<button type="submit" class="btn btn-primary">Submit</button>
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

	<!-- end row -->

</section>
<!-- end widget grid -->

<script type="text/javascript">
	// PAGE RELATED SCRIPTS
	$('#updatesensor-form').submit(function(e){
		$.post("<?=base_url('register/update_sensor')?>", $( "#updatesensor-form" ).serialize()).done(function(data) {
            if(data == '0'){
                alert('please fill ');
            }else{
                window.location.href="<?=base_url('register')?>";
            }
		});
		return false;
	});

</script>
