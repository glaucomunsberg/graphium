class Graphium::ClassificationController < ApplicationController
  respond_to :json, :html, :js
  before_filter :authenticate_user!
  layout "inside"

  require 'net/http'

  def index

  end

  def getInformation

    @informations = {}

    @classifications = []
    if params[:true] == "true"
      @classifications << "T"
    end
    if params[:false] == "true"
      @classifications << "F"
    end

    if params[:true_negative] == "true"
      @classifications << "TN"
    end

    if params[:true_positive] == "true"
      @classifications << "TP"
    end

    if params[:false_negative] == "true"
      @classifications << "FN"
    end

    if params[:false_positive] == "true"
      @classifications << "FP"
    end

    #logger.info "Classification wanted"
    #logger.info @classifications

    panos = Graphium::Pano.where(:classification.in => @classifications ).length
    @informations['pano'] = panos[params[:pano_position].to_i]
    @informations['total'] = panos.length
    @informations['classifications'] = @classifications
    respond_to do |format|
      format.json { render :json => @informations }
    end
  end

  def updatePano

    @pano = Graphium::Pano.where(:pano_id => params[:pano_id],:heading => params[:heading]).first
    @pano.classification = params[:pano_classification]
    @pano.save

    if params[:pano_classification] == "FP"
      Graphium::Graffiti.where(:pano_id => params[:pano_id]).each do | graphium |
        if graphium.heading.to_i == params[:heading].to_i
          graphium.situation = "false_positive"
          graphium.save
        end
      end
    elsif params[:pano_classification] == "FN"
        Graphium::Pano.where(:pano_id => params[:pano_id]).each do | pano |
          if pano.heading.to_i == params[:heading].to_i

            uri = URI("https://maps.googleapis.com/maps/api/streetview/metadata?key=#{Graphium::Configuration.first.google_maps_key}&pano=#{params[:pano_id]}")
            response = Net::HTTP.get(uri)
            gmaps_pano_id = JSON.parse(response)


            uri = URI("https://nominatim.openstreetmap.org/reverse?format=json&osm_type=W&lat=#{gmaps_pano_id['location']['lat']}&lon=#{gmaps_pano_id['location']['lng']}")
            response = Net::HTTP.get(uri)
            open_data_id = JSON.parse(response)

            graffiti = Graphium::Graffiti.new
            graffiti.city = open_data_id['address']['city']
            graffiti.state = open_data_id['address']['state']
            graffiti.lat = gmaps_pano_id['location']['lat']
            graffiti.lng = gmaps_pano_id['location']['lng']
            graffiti.country = open_data_id['address']['country']
            graffiti.pitch = pano.splited
            graffiti.heading = pano.heading
            graffiti.address = open_data_id['address']['road']
            graffiti.pano_id = pano.pano_id
            graffiti.situation = "false_negative"
            graffiti.save

          end
        end
    elsif params[:pano_classification] == "TP"
      Graphium::Graffiti.where(:pano_id => params[:pano_id]).each do | graphium |
        if graphium.heading.to_i == params[:heading].to_i
          graphium.situation = "true_positive"
          graphium.save
        end
      end
    end
    respond_to do |format|
      format.json { render :json => @pano }
    end
  end

end
