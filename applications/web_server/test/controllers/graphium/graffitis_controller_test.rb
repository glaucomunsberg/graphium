require 'test_helper'

class Graphium::GraffitisControllerTest < ActionController::TestCase
  setup do
    @graphium_graffiti = graphium_graffitis(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:graphium_graffitis)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create graphium_graffiti" do
    assert_difference('Graphium::Graffiti.count') do
      post :create, graphium_graffiti: { address: @graphium_graffiti.address, city: @graphium_graffiti.city, country: @graphium_graffiti.country, heading: @graphium_graffiti.heading, lat: @graphium_graffiti.lat, lng: @graphium_graffiti.lng, pitch: @graphium_graffiti.pitch, state: @graphium_graffiti.state }
    end

    assert_redirected_to graphium_graffiti_path(assigns(:graphium_graffiti))
  end

  test "should show graphium_graffiti" do
    get :show, id: @graphium_graffiti
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @graphium_graffiti
    assert_response :success
  end

  test "should update graphium_graffiti" do
    patch :update, id: @graphium_graffiti, graphium_graffiti: { address: @graphium_graffiti.address, city: @graphium_graffiti.city, country: @graphium_graffiti.country, heading: @graphium_graffiti.heading, lat: @graphium_graffiti.lat, lng: @graphium_graffiti.lng, pitch: @graphium_graffiti.pitch, state: @graphium_graffiti.state }
    assert_redirected_to graphium_graffiti_path(assigns(:graphium_graffiti))
  end

  test "should destroy graphium_graffiti" do
    assert_difference('Graphium::Graffiti.count', -1) do
      delete :destroy, id: @graphium_graffiti
    end

    assert_redirected_to graphium_graffitis_path
  end
end
