<?php
header("Content-Type: application/json");
include 'db_config.php';

$data = [];
$total_helm_false = 0;
$total_strap_false = 0;

$sql = "SELECT * FROM log_history ORDER BY id DESC";
$result = $conn->query($sql);

while ($row = $result->fetch_assoc()) {
    if ($row['status_helm'] == 0) $total_helm_false++;
    if ($row['status_strap'] == 0) $total_strap_false++;

    $data[] = $row;
}

echo json_encode([
    "log_history" => $data,
    "total_helm_false" => $total_helm_false,
    "total_strap_false" => $total_strap_false
]);
?>
