#sends data to data lake. Provide the drop zone bucket as the first argument to the command line.
aws s3 cp order_items.csv   s3://2ndwatch-datalake-demo-drop-486567699039/order_items/
aws s3 cp order_reviews.csv s3://2ndwatch-datalake-demo-drop-486567699039/order_reviews/
aws s3 cp orders.csv        s3://2ndwatch-datalake-demo-drop-486567699039/orders/
aws s3 cp sellers.csv       s3://2ndwatch-datalake-demo-drop-486567699039/sellers/
