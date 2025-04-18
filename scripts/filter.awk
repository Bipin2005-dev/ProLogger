BEGIN {
	FS=",";
	OFS=",";
}

// {
	datetime=$7
	if (datetime >= start_datetime && datetime <= end_datetime) {
		print $1,$2,$3,$4,$5,$6;
	}
}
