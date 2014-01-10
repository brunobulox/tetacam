<?php

    require_once('../preheader.php'); // <-- this include file MUST go first before any HTML/output

    #the code for the class
    include ('./ajaxcrud/ajaxCRUD.class.php'); // <-- this include file MUST go first before any HTML/output

?>
<img src="images/tetacam_logo.jpg" alt="Teta" height="80" width="260" align="right">
<div id='cssmenu'>
<ul>  
   <li><a href='?page=contacts'><span>Contacts</span></a></li>
   <li><a href='?page=events'><span>Event log</span></a></li>
   <li><a href='http://192.168.1.67:8000' target='_blank'><span>Cam view</span></a></li>
   <li><a href='?page=admin'><span>Admin</span></a></li>   
</ul>
</div>

<?

    $page=$_GET["page"];
    if ($page == "contacts"){
        $tblContacts = new ajaxCRUD("Item", "contacts", "userid", "../");

        $tblContacts->omitPrimaryKey();

        #Display field name mappings
        $tblContacts->displayAs("name", "Name");
        $tblContacts->displayAs("phone", "Phone");
        $tblContacts->displayAs("phoneactive", "Phone active");
        $tblContacts->displayAs("text", "Text");
        $tblContacts->displayAs("textactive", "Text active");
        $tblContacts->displayAs("email", "Email");
        $tblContacts->displayAs("emailactive", "Email active");
   
        $tblContacts->addOrderBy("ORDER BY name ASC");
        $tblContacts->setLimit(30);
        $tblContacts->formatFieldWithFunction('name', 'makeBold');
        //set field fldCheckbox to be a checkbox
        $tblContacts->defineCheckbox("phoneactive");
        $tblContacts->defineCheckbox("textactive");
        $tblContacts->defineCheckbox("emailactive");

        #show the table
	$tblContacts->showTable();

        } 
	
	elseif ($page == "events"){

	$tblEvents = new ajaxCRUD("Item", "motion_log", "event_number", "../");

        //$tblEvents->omitPrimaryKey();
        $tblEvents->omitField("frame");
	$tblEvents->omitField("event_time_stamp");
	$tblEvents->omitField("file_type");

        #Display field name mappings
        $tblEvents->displayAs("event_number", "Event Number");
        $tblEvents->displayAs("filename", "File created");
        $tblEvents->displayAs("time_stamp", "Time Stamp");
        $tblEvents->displayAs("camera", "Camera number");
   
        $tblEvents->addOrderBy("ORDER BY event_number DESC");
        $tblEvents->setLimit(30);
        $tblEvents->disallowDelete();
        //$tblContacts->formatFieldWithFunction('name', 'makeBold');

	#show the table
	$tblEvents->showTable();

	}

	#my self-defined functions used for formatFieldWithFunction
	function makeBold($val){
		return "<b>$val</b>";
	}

	function makeBlue($val){
		return "<span style='color: blue;'>$val</span>";
	}

	function myCallBackFunction($array){
		echo "THE ADD ROW CALLBACK FUNCTION WAS implemented";
		print_r($array);
	}
?>
