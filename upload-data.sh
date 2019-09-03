#sends data to data lake. Provide the drop zone bucket as the first argument to the command line.
aws s3 cp $1'olist_order_items_dataset.csv' $2'order-items/'
aws s3 cp $1'olist_order_reviews_dataset.csv' $2'order-reviews/'
aws s3 cp $1'olist_closed_deals_dataset.csv' $2'closed-deals/'
aws s3 cp $1'olist_sellers_dataset.csv' $2'sellers/'
