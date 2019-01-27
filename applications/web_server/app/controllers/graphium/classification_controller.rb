class Graphium::ClassificationController < ApplicationController
  respond_to :json, :html, :js
  before_filter :authenticate_user!
  layout "inside"

  require 'net/http'

  def index

  end

  def getInformation

    @informations = {}

    @classifications = ""
    if params[:true] == "true"
      @classifications = "T"
    elsif params[:false] == "true"
      @classifications = "F"
    elsif params[:true_negative] == "true"
      @classifications = "TN"
    elsif params[:true_positive] == "true"
      @classifications = "TP"
    elsif params[:false_negative] == "true"
      @classifications = "FN"
    elsif params[:false_positive] == "true"
      @classifications = "FP"
    end

    #logger.info "Classification wanted"
    #logger.info @classifications

    if params[:swarm_identifier] == "" or params[:swarm_identifier] == "Todos"
      panos = Graphium::Pano.where(:classification => @classifications ).limit(400)
    else
      panos = Graphium::Pano.where(:classification => @classifications, :swarm_identifier => params[:swarm_identifier] ).limit(400)
    end

    @informations['pano'] = panos[params[:pano_position].to_i]
    @informations['total'] = panos.length
    @informations['classifications'] = @classifications
    @informations['similar_classifications'] = []
    if not @informations['pano'].nil?
      Graphium::Pano.where(:pano_id => @informations['pano'].pano_id).each do | pano_similar |
        if pano_similar.swarm_identifier != @informations['pano'].swarm_identifier and pano_similar.heading.to_i == @informations['pano'].heading.to_i
          @informations['similar_classifications'].push pano_similar.classification
        end
      end
    end
    if params[:pano_position].to_i == 0
      @informations['classifieds'] = {}
      @informations['classifieds']['TP'] = Graphium::Pano.where(:classification => 'TP' ).length
      @informations['classifieds']['FP'] = Graphium::Pano.where(:classification => 'FP' ).length
      @informations['classifieds']['TN'] = Graphium::Pano.where(:classification => 'TN' ).length
      @informations['classifieds']['FN'] = Graphium::Pano.where(:classification => 'FN' ).length
      @informations['classifieds']['T'] = Graphium::Pano.where(:classification => 'T' ).length
      @informations['classifieds']['F'] = Graphium::Pano.where(:classification => 'F' ).length
    end

    @informations['results'] = {}
    @informations['results']['true'] = Graphium::Pano.where(:classification => ['T', 'FP', 'TP'], :swarm_identifier => params[:swarm_identifier] ).length
    @informations['results']['false'] = Graphium::Pano.where(:classification => ['F', 'FN', 'TN'], :swarm_identifier => params[:swarm_identifier] ).length
    @informations['results']['true_positive'] = Graphium::Pano.where(:classification => "TP", :swarm_identifier => params[:swarm_identifier] ).length
    @informations['results']['true_negative'] = Graphium::Pano.where(:classification => "TN", :swarm_identifier => params[:swarm_identifier] ).length
    @informations['results']['false_positive'] = Graphium::Pano.where(:classification => "FP", :swarm_identifier => params[:swarm_identifier] ).length
    @informations['results']['false_negative'] = Graphium::Pano.where(:classification => "FN", :swarm_identifier => params[:swarm_identifier] ).length
    @informations['results']['sensibility'] = (@informations['results']['true_positive'].to_f / (@informations['results']['true_positive']+@informations['results']['false_positive']).to_f).round(4)
    @informations['results']['especificility'] = (@informations['results']['true_negative'].to_f / (@informations['results']['false_negative']+@informations['results']['true_negative']).to_f).round(4)
    @informations['results']['preditive_positive'] = (@informations['results']['false_positive'].to_f / (@informations['results']['false_positive']+@informations['results']['false_negative']).to_f).round(4)
    @informations['results']['preditive_negative'] = (@informations['results']['true_negative'].to_f / (@informations['results']['false_positive']+@informations['results']['true_negative']).to_f).round(4)

    respond_to do |format|
      format.json { render :json => @informations }
    end
  end

  def updatePano

    @pano = Graphium::Pano.find(params[:pano_id_mongo])
    @pano.classification = params[:pano_classification]
    @pano.save

    if params[:pano_classification] == "FP"
      Graphium::Graffiti.where(:pano_id => params[:pano_id], :swarm_identifier => params[:swarm_identifier]).each do | graphium |
        if graphium.heading.to_i == params[:heading].to_i
          graphium.situation = "false_positive"
          graphium.save!
        end
      end
    elsif params[:pano_classification] == "FN"

        #pano = Graphium::Pano.find(params[:pano_id_mongo])

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
        graffiti.pitch = @pano.splited
        graffiti.heading = @pano.heading.to_f
        graffiti.address = open_data_id['address']['road']
        graffiti.pano_id = @pano.pano_id
        graffiti.situation = "false_negative"
        graffiti.swarm_identifier = params[:swarm_identifier]
        graffiti.save!

    elsif params[:pano_classification] == "TP"
      Graphium::Graffiti.where(:pano_id => params[:pano_id], :swarm_identifier => params[:swarm_identifier]).each do | graphium |
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


  def compare
    @panos = {}
    @swarms = []
    Graphium::Swarm.where(:city_id => "5c3e625c2c222969abddd6ca").each do | swarm |
      @swarms.push swarm.identifier
      Graphium::Graffiti.where(:swarm_identifier => swarm.identifier).each do | graffiti |
        key_pano = graffiti.pano_id+"_"+graffiti.heading.to_i.to_s
        if @panos.key? key_pano
          if not @panos[key_pano]['swarms'].include? swarm.identifier
            @panos[key_pano]['swarms'].push swarm.identifier
          end
        else
          @panos[key_pano] = {}
          @panos[key_pano]['pano'] = {"pano_id": graffiti.pano_id, "heading": graffiti.heading, "lat":graffiti.lat, "lng":graffiti.lng, "pitch": graffiti.pitch}
          @panos[key_pano]['swarms'] = []
          @panos[key_pano]['swarms'].push swarm.identifier
        end
      end
    end
  end

end
