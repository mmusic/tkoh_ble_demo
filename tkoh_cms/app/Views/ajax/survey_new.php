<!-- widget grid -->
<section id="widget-grid" class="">

	<!-- row -->
	<div class="row">

		<!-- NEW WIDGET START -->
		<article class="col-xs-12 col-sm-12 col-md-12 col-lg-6">

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
					<h2>New Survey Event</h2>

				</header>

				<!-- widget div-->
				<div>
					<div class="widget-body no-padding">
						<form id="newevent-form" class="smart-form">
							<header>Check form</header>
							<fieldset>
                                <section>
                                    <label class="label">Event ID</label>
                                    <label class="input state-success"> <i class="icon-prepend fa fa-barcode"></i>
                                        <input type="text" name="event" value="<?=$ts?>" placeholder="<?=$ts?>">
                                    </label>
                                </section>
                                <section>
                                    <label class="label">Date</label>
                                    <label class="input state-success"> <i class="icon-prepend fa  fa-calendar"></i>
                                        <input type="tel" name="date" value="<?=$date?>" placeholder="<?=$date?>" data-mask="9999-99-99">
                                    </label>
                                </section>
                                <section>
									<label class="label">Site</label>
                                    <label class="input state-success"> <i class="icon-prepend fa fa-location-arrow"></i>
                                        <input type="text" name="site" placeholder="Site Name">
                                    </label>
                                </section>
								<section>
									<label class="label">Remmark</label>
									<input type="hidden" name="id" value="<?= $id ?>">
									<label class="textarea state-info" >
										<textarea rows="4" name="remark" ></textarea>
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
	$('#newevent-form').submit(function(e){
		$.post("<?=base_url('survey/add_event')?>", $( "#newevent-form" ).serialize()).done(function(data) {
            if(data == '0'){
                alert('please fill ');
            }else{
                window.location.href="<?=base_url('survey/event').'/'?>" + data;
            }
		});
		return false;
	});
</script>
