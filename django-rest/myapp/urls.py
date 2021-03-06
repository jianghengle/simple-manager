from django.urls import path
from .views.custom_auth_token import CustomAuthToken
from .views import user_view
from .views import cost_view
from .views import s3_view
from .views import attachment_view
from .views import my_config_view
from .views import vendor_subsidiary_view
from .views import product_price_view

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('get-all-emails/', user_view.get_all_emails, name='get-all-emails'),
    path('create-password-reset/', user_view.create_password_reset, name='create-password-reset'),
    path('get-password-reset-by-key/<str:key>/', user_view.get_password_reset_by_key, name='get-password-reset-by-key'),
    path('change-password/<str:key>/', user_view.change_password, name='change-password'),
    path('get-costs/', cost_view.get_costs, name='get-costs'),
    path('get-cost/<str:cost_id>/', cost_view.get_cost, name='get-cost'),
    path('create-cost/', cost_view.create_cost, name='create-cost'),
    path('update-cost/<str:cost_id>/', cost_view.update_cost, name='update-cost'),
    path('delete-cost/<str:cost_id>/', cost_view.delete_cost, name='delete-cost'),
    path('send-email-for-cost/<str:cost_id>/', cost_view.send_email_for_cost, name='send-email-for-cost'),
    path('get-s3-upload-url/', s3_view.get_upload_url, name='get-s3-upload-url'),
    path('get-s3-download-url/', s3_view.get_download_url, name='get-s3-download-url'),
    path('create-attachment/', attachment_view.create_attachment, name='create-attachment'),
    path('get-attachment/<str:attachment_id>/', attachment_view.get_attachment, name='get-attachment'),
    path('get-my-config/', my_config_view.get_my_config, name='get-my-config'),
    path('update-my-config/', my_config_view.update_my_config, name='update-my-config'),
    path('get-vendor-subsidiaries/', vendor_subsidiary_view.get_vendor_subsidiaries, name='get-vendor-subsidiaries'),
    path('get-products-with-latest-prices/', product_price_view.get_products_with_latest_prices, name='get-products-with-latest-prices'),
    path('get-product-with-prices/<str:product_id>/', product_price_view.get_product_with_prices, name='get-product-with-prices'),
    path('update-product-latest-price/<str:product_id>/<str:channel_id>/', product_price_view.update_product_latest_price, name='update-product-latest-price'),
    path('update-product-by-model/', product_price_view.update_product_by_model, name='update-product-by-model'),
]
