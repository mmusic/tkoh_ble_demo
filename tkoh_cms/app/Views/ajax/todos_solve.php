<div id="done"> </div>
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
					<h2>TODOS</h2>
				</header>
				<!-- widget div-->
				<?php if($todos_item['todo'] == '0'){; ?>
				<div>
					<div class="table-responsive">
						<table class="table table-bordered hidden-mobile">
							<thead>
								<tr>
									<th>Date</th>
									<th>scr_type</th>
								</tr>
							</thead>
							<tbody>
								<tr class="danger">
									<td><strong><?= date('Y/m/d H:i:s', $todos_item['ts']/1000)?></strong></td>
									<td><strong>
										<code>
											<?= $todos_item['src_type'] ?>
										</code></strong>
									</td>
								</tr>
							</tbody>
						</table>
						<h4>Content</h4>
						<table class="table table-bordered hidden-mobile">
							<tbody>
								<?php foreach (json_decode($todos_item['content']) as $key => $value) { ?>
									<tr class="warning">
									<td><strong><?= $key ?></strong></td>
									<td><?= $value ?></td>
									</tr>
								<?php }?>
							</tbody>
						</table>
					</div>
					<div class="widget-body no-padding">
						<form id="updatetodo-form" class="smart-form">
							<fieldset>
								<section>
									<h4>Solve Message</h4>
									<input type="hidden" name="id" value="<?= $todos_item['id'] ?>">
									<label class="textarea state-success" >
										<textarea rows="4" name="solve_msg" id="reporting_message" ></textarea>
									</label>
									<div class="note note-error">This is a required field.</div>
								</section>
								<section>
									<label class="checkbox"><input type="checkbox" name="copy" id="checkbox" disabled><i></i>###</label>
								</section>
							</fieldset>

							<footer>
								<button type="submit" class="btn btn-primary">Submit</button>
							</footer>
						</form>
					</div>
				</div>
				<?php }else{ ?>
				 <div>
					<div class="table-responsive">
						<table class="table table-bordered hidden-mobile">
							<thead>
								<tr>
									<th>Date</th>
									<th>scr_type</th>
									<th>content</th>
									<th>msg</th>
								</tr>
							</thead>
							<tbody>
								<tr class="success">
									<td><?= date('Y/m/d H:i:s', $todos_item['ts']/1000)?></td>
									<td>
										<code>
											<?= $todos_item['src_type'] ?>
										</code
									></td>
									<td><?= $todos_item['content'] ?></td>
									<td><?= $todos_item['solve_msg'] ?></td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
				<?php } ?>
				<!-- end widget div -->

			</div>
			<!-- end widget -->

		</article>
		<!-- WIDGET END -->


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
					<h2>Relate </h2>

				</header>

				<!-- widget div-->
				<div>

					<!-- widget edit box -->
					<div class="jarviswidget-editbox">
						<!-- This area used as dropdown edit box -->

					</div>
					<!-- end widget edit box -->

					<!-- widget content -->
					<div class="widget-body no-padding">

						<table class="table table-bordered">
							<thead>
								<tr>
									<th> <i class="fa fa-building"></i> SRC_TYPE </th>
									<th> <i class="fa fa-calendar"></i> Content</th>
									<th> <i class="fa fa-calendar"></i> Sovle MSG</th>
									<th> <i class="glyphicon glyphicon-send"></i> TODO </th>
								</tr>
							</thead>
							<tbody>
							    <?php if ($related_logs) {foreach($related_logs as $log){
							        if($log->todo==1)
							        {
							        }
							        elseif($log->todo==0)
							        {
							        }
							    // todo: if the todo is null, then make it grey, if it's done, make a green tick, otherwise make it empty
// 							        echo " <tr class=\"info\">
//                                             <td>{$log->src_type}</td>
//                                             <td>{$log->content}</td>
//                                             <td>{$log->solve_message}</td>
//                                             <td>{$log->todo}</td>
//                                         </tr>";
// 					             echo " <tr class=\"info\">
//                                             <td>{$log->src_type}</td>
//                                             <td>{$log->content}</td>
//                                             <td>{$log->solve_message}</td>
//                                             <td class=\"text-align-center demo-icon-font bg-color-grey\">
// 										        <i class=\"fa fa-check\"></i>
//
// 										    </td>
//                                         </tr>";
					             echo " <tr class=\"info\">
                                            <td>{$log->src_type}</td>
                                            <td>{$log->content}</td>
                                            <td>{$log->solve_message}</td>
                                            <td class=\"bg-color-grayLLight\"></td>
                                        </tr>";
							        }
							    }
							        ?>
							</tbody>
						</table>

					</div>
					<!-- end widget content -->

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
	// DO NOT REMOVE : GLOBAL FUNCTIONS!
	pageSetUp();

	// PAGE RELATED SCRIPTS
	$('#updatetodo-form').submit(function(e){
		$.post("<?= base_url('maintenance/update_todos') ?>", $("#updatetodo-form").serialize()).done(function(data) {
			console.log(data);
			// $('#done').html(data);
			setTimeout(window.location.reload(), 3000);
		});
		return false;
	});

</script>
