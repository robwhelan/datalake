#sends data to data lake. Provide the drop zone bucket as the first argument to the command line.
aws s3 cp ../ecommerce-data/olist_order_items_dataset.csv   s3://datalake-demo-drop-773548596459/order-items/
aws s3 cp ../ecommerce-data/olist_order_reviews_dataset.csv s3://datalake-demo-drop-773548596459/order-reviews/
aws s3 cp ../ecommerce-data/olist_closed_deals_dataset.csv  s3://datalake-demo-drop-773548596459/closed-deals/
aws s3 cp ../ecommerce-data/olist_sellers_dataset.csv       s3://datalake-demo-drop-773548596459/sellers/
