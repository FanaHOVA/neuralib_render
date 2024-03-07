import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, Literal

load_dotenv()

class ListAllServices(BaseModel):
    """List all cloud services the user is hosting on Render.com"""
    limit: int = Field(default=20, description="The max number of services to return.")

class CreateService(BaseModel):
    """Create a new cloud service for the user on Render.com"""
    name: str = Field(default="my-new-service", description="The name of the service to create.")
    service_type: Literal['cron_job', 'web_service', 'background_worker', 'private_service', 'static_site'] = Field(default="web", description="The type of service to create.")
    service_details: dict = Field(default={}, description="The service details to set for the service. For example for a cron job: { 'env': 'docker', 'schedule': '0 0 * * *' }")


class Render:
  @staticmethod
  def authorization_headers():
    return {
        'Accept': 'application/json',
        'Authorization': f'Bearer {os.getenv("RENDER_API_KEY")}'
      }
  
  def list_all_services(limit=20):
      url = f'https://api.render.com/v1/services?limit={limit}'

      response = requests.get(url, headers=Render.authorization_headers())

      print(response.json())
      
  def create_service(name='my-new-service', service_type='cron_job', service_details={ "env": "docker", "schedule": "0 0 * * *" }):
      url = 'https://api.render.com/v1/services'
      
      data = {
        "ownerId": os.getenv("RENDER_OWNER_ID"),
        "name": name,
        "type": service_type,
        "serviceDetails": service_details
      }

      response = requests.post(url, headers=Render.authorization_headers(), json=data)

      print(response.json())
      
  @staticmethod
  def functions():
    return [
      ListAllServices.model_json_schema()
    ]