<!DOCTYPE html>
<html lang="en-us">
	<head>
		<meta charset="utf-8">
		<!--<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">-->
		
		<title> SmartAdmin </title>
		<meta name="description" content="">
		<meta name="author" content="">
		
		<!-- http://davidbcalhoun.com/2010/viewport-metatag -->
		<meta name="HandheldFriendly" content="True">
		<meta name="MobileOptimized" content="320">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
		
		<!-- Basic Styles -->	
		<link rel="stylesheet" type="text/css" media="screen" href="<?= base_url('/public/css/bootstrap.min.css')?>">	
		<link rel="stylesheet" type="text/css" media="screen" href="<?= base_url('/public/css/font-awesome.min.css')?>">
	
		<!-- SmartAdmin Styles : Please note (smartadmin-production.css) was created using LESS variables -->
		<link rel="stylesheet" type="text/css" media="screen" href="<?= base_url('/public/css/smartadmin-production.css')?>">
		<link rel="stylesheet" type="text/css" media="screen" href="<?= base_url('/public/css/smartadmin-skins.css')?>">	
		
		<!-- SmartAdmin RTL Support is under construction
			<link rel="stylesheet" type="text/css" media="screen" href="css/smartadmin-rtl.css"> -->
		
		<!-- Demo purpose only: goes with demo.js, you can delete this css when designing your own WebApp -->
		<link rel="stylesheet" type="text/css" media="screen" href="<?= base_url('/public/css/demo.css')?>">
		
		<!-- FAVICONS -->
		<link rel="shortcut icon" href="<?= base_url('/public/img/favicon/favicon.ico')?>" type="image/x-icon">
		<link rel="icon" href="<?= base_url('/public/img/favicon/favicon.ico')?>" type="image/x-icon">
		
		<!-- GOOGLE FONT -->
		<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Open+Sans:400italic,700italic,300,400,700">

		<!-- MAPBOX -->
		<link href="<?= base_url('/public/css/mapbox/mapbox-gl.css')?>" rel="stylesheet" />
		<link href="<?= base_url('/public/css/mapbox/mapbox-gl-app.css')?>" rel="stylesheet" />
		<link rel="stylesheet" type="text/css" href="<?=base_url('public/css/DataTables-1.10.22/css/dataTables.bootstrap.min.css')?>"/>
	</head>
	<body class=""> <!-- possible classes: minified, fixed-ribbon, fixed-header, fixed-width-->
		
		<!-- HEADER -->
		<header id="header">
				<div id="logo-group">

                    <!-- PLACE YOUR LOGO HERE -->
                    <span id="logo">
						<!-- <img src="" alt="SmartAdmin"> -->
						<Strong>DEMO</strong>
                    </span>
                    <!-- END LOGO PLACEHOLDER -->

				</div>
				<!-- END AJAX-DROPDOWN -->
			</div>

			
			<!-- pulled right: nav area -->
			<div class="pull-right">
				
				<!-- collapse menu button -->
				<div id="hide-menu" class="btn-header pull-right">
					<span>
						<a href="javascript:void(0);" title="Collapse Menu"><i class="fa fa-reorder"></i></a>
					</span>
				</div>
				<!-- end collapse menu -->
				
				<!-- logout button -->
				<div id="logout" class="btn-header transparent pull-right">
					<span>
						<a href="#" title="Sign Out"><i class="fa fa-sign-out"></i></a>
					</span>
				</div>
				<!-- end logout button -->
			
			</div>
			<!-- end pulled right: nav area -->
			
		</header>
		<!-- END HEADER -->
		
		<!-- Left panel : Navigation area -->
		<!-- Note: This width of the aside area can be adjusted through LESS variables -->
		<aside id="left-panel">
			
			<!-- User info -->
			<div class="login-info">
				<span>
					<!-- User image size is adjusted inside CSS, it should stay as it --> 
					<!-- <img src="" alt="me" class="online" /> -->
					<a href="javascript:void(0);">Welcome: Admin</a>
				</span>
			</div>
			<!-- end user info -->
			<nav>
				<ul>
					<li class=""><a href="<?=base_url()?>" title="dashboard"><i class="fa fa-lg fa-fw fa-home"></i>  <span class="menu-item-parent">Dashboard</span></a></li>
					<li><a href="<?=base_url('maintenance')?>">
						<i class="fa fa-lg fa-fw fa-check-circle-o"></i>  
						<span class="menu-item-parent">Maintenance</span></a>
					</li>
					<li class=""><a href="#" title="Analysis"><i class="fa fa-lg fa-fw fa-file-text"></i>  <span class="menu-item-parent">Analysis</span></a></li>
					<li class=""><a href="#" title="Monitor"><i class="fa fa-lg fa-fw fa-desktop"></i>  <span class="menu-item-parent">Monitor</span></a>
						<ul>
							<?php foreach($site_names as $site_name){?>
							<li><a href="<?=base_url('monitor').'/'.$site_name['site_name']?>"><?= $site_name['site_name']?></a></li>
							<?php } ?>
						</ul>
					</li>
					<li><a href="#"><i class="fa fa-lg fa-fw fa-gear"></i>  <span class="menu-item-parent">Tools</span></a>
						<ul>
							<li><a href="<?=base_url('polygon')?>">Polygon</a></li>
							<li><a href="#">Survey</a></li>
							<li><a href="<?=base_url('register')?>">Register</a></li>
						</ul>
					</li>
					
				</ul>
			</nav>
			<span class="minifyme">
				<i class="fa fa-arrow-circle-left hit"></i>
			</span>

			
		</aside>
		<!-- END NAVIGATION -->
		
		<!-- MAIN PANEL -->
		<div id="main" role="main">
			
			<!-- RIBBON -->
			<div id="ribbon">
				<span class="ribbon-button-alignment">
					<lable class="txt-color-white"><div id="time"></div></lable>
				</span>
			</div>
			<!-- END RIBBON -->
			
			<!-- MAIN CONTENT -->
			<div id="content">
				<div class="row">
					<div class="col-xs-12 col-sm-7 col-md-7 col-lg-4">
						<h1 class="page-title txt-color-blueDark">
							<i class="fa <?=$icon?> fa-fw "></i> 
								<a href="<?=base_url($title)?>" style="color:#696969; cursor:pointer"><strong><?=$title?></strong></a> 
							<span>
								<strong style="color:#496949"><?= $sub_title?></strong>
							</span>
						</h1>
					</div>
					<div class="col-xs-12 col-sm-5 col-md-5 col-lg-8">
						<ul id="sparks" class="">
							<li class="sparks-info">
								<h5> CPU <span class="txt-color-blue"><label id="cpu"></label></span></h5>
							</li>
							<li class="sparks-info">
								<h5> MEMORY <span class="txt-color-purple"><label id="memory"></label></span></h5>
							</li>
							<li class="sparks-info">
								<h5> STORAGE <span class="txt-color-greenDark"><label id="storage"></label></span></h5>
							</li>
						</ul>
					</div>
				</div>
